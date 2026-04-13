"""
HandTracker — state machine that infers hand progression from card visibility.

Since we have no OCR, we can only observe:
  - Which cards are visible (label != "empty" / "back" / "unknown")
  - How many community cards are on the board (0/3/4/5)

From this we infer:
  - When a new hand starts (hero cards appear after being absent)
  - Which street we're on (preflop / flop / turn / river)
  - Which seats stayed in the hand (had visible cards at each street transition)
  - When a hand ends (hero cards disappear)

This is a best-effort estimation. Stats are labeled as "estimated" in the UI.
"""

import time
from dataclasses import dataclass, field
from typing import Optional

from src.capture.pipeline import FrameResult
from src.common.constants import SPECIAL_LABELS
from src.tracking.database import HandRecord, PokerDB


@dataclass
class _HandState:
    """Mutable state for the current in-progress hand."""
    started_at: float = 0.0
    street: str = "preflop"
    board_seen: list[str] = field(default_factory=list)
    # seat -> {preflop, flop, turn, river, total_thinking_time, turn_action_count}
    seat_participation: dict[str, dict] = field(default_factory=dict)
    current_turn_seat: Optional[str] = None
    turn_started_at: float = 0.0


def _count_known_board(board_labels: list[tuple[str, float]]) -> int:
    return sum(1 for label, _ in board_labels if label not in SPECIAL_LABELS)


def _has_hero_cards(hero_labels: list[tuple[str, float]]) -> bool:
    return any(label not in SPECIAL_LABELS for label, _ in hero_labels)


def _street_from_count(n: int) -> str:
    if n == 0:
        return "preflop"
    elif n == 3:
        return "flop"
    elif n == 4:
        return "turn"
    else:
        return "river"


class HandTracker:
    """
    Processes FrameResults and maintains hand state.
    Records completed hands to the database.
    """

    def __init__(self, db: PokerDB, seat_keys: list[str]) -> None:
        """
        Args:
            db:        PokerDB instance for recording completed hands.
            seat_keys: List of seat region keys to track (e.g. ["seat_1_card_1", ...]).
                       Pairs of seat cards are grouped by seat name.
        """
        self._db = db
        self._seats = self._parse_seats(seat_keys)  # seat_name -> [card_key1, card_key2]
        self._state: Optional[_HandState] = None
        self._prev_had_hero = False
        self._prev_board_count = 0

    @staticmethod
    def _parse_seats(seat_keys: list[str]) -> dict[str, list[str]]:
        """Group card keys by seat name. seat_1_card_1, seat_1_card_2 -> seat_1: [...]"""
        seats: dict[str, list[str]] = {}
        for key in seat_keys:
            # key format: seat_{n}_card_{m}
            parts = key.rsplit("_card_", 1)
            if len(parts) == 2:
                seat_name = parts[0]
                seats.setdefault(seat_name, []).append(key)
        return seats

    def update(self, result: FrameResult) -> None:
        """
        Process a new FrameResult. Call once per capture cycle.
        Automatically records completed hands to the database.
        """
        if not result.window_found:
            return

        # Extract hero and board info
        hero_labels = list(result.hero_cards)  # list of (label, confidence)
        board_raw = list(result.community_cards)
        board_count = _count_known_board(board_raw)
        has_hero = _has_hero_cards(hero_labels)
        board_labels = [label for label, _ in board_raw if label not in SPECIAL_LABELS]
        current_street = _street_from_count(board_count)

        # --- Hand boundary detection ---

        # New hand: hero cards appeared (were absent in previous frame)
        if has_hero and not self._prev_had_hero:
            if self._state is not None:
                # Flush previous hand if it didn't close cleanly
                self._commit_hand(self._state)
            self._state = _HandState(started_at=time.time())
            self._state.street = "preflop"
            # Initialize participation for all tracked seats
            for seat in self._seats:
                self._state.seat_participation[seat] = {
                    "stayed_preflop": True,  # assume in until we see otherwise
                    "stayed_flop": False,
                    "stayed_turn": False,
                    "stayed_river": False,
                    "total_thinking_time": 0.0,
                    "turn_action_count": 0,
                }

        # Hand ended: hero cards disappeared (were present in previous frame)
        if not has_hero and self._prev_had_hero and self._state is not None:
            self._commit_hand(self._state)
            self._state = None

        # Update street and seat participation
        if self._state is not None and has_hero:
            self._state.board_seen = board_labels
            self._state.street = current_street

            # Determine active seat
            current_active_seat = None
            for key, (label, conf) in result.cards.items():
                if "_active" in key and label not in SPECIAL_LABELS:
                    current_active_seat = key.split("_active")[0]
                    break
            
            # Handle turn transition
            if self._state.current_turn_seat != current_active_seat:
                if self._state.current_turn_seat is not None:
                    duration = time.time() - self._state.turn_started_at
                    part = self._state.seat_participation.get(self._state.current_turn_seat)
                    if part is not None:
                        part["total_thinking_time"] += duration
                        part["turn_action_count"] += 1
                
                self._state.current_turn_seat = current_active_seat
                self._state.turn_started_at = time.time()

            # Track which seats still have visible cards per street
            for seat, card_keys in self._seats.items():
                has_seat_cards = any(
                    result.cards.get(k, ("empty", 0))[0] not in SPECIAL_LABELS
                    for k in card_keys
                )
                if current_street == "flop" and board_count >= 3:
                    if has_seat_cards:
                        self._state.seat_participation[seat]["stayed_flop"] = True
                elif current_street == "turn" and board_count >= 4:
                    if has_seat_cards:
                        self._state.seat_participation[seat]["stayed_turn"] = True
                elif current_street == "river" and board_count >= 5:
                    if has_seat_cards:
                        self._state.seat_participation[seat]["stayed_river"] = True

        self._prev_had_hero = has_hero
        self._prev_board_count = board_count

    def _commit_hand(self, state: _HandState) -> None:
        """Write a completed hand record to the database."""
        record = HandRecord(
            session_id=self._db.session_id or 0,
            street_reached=state.street,
            board_cards=state.board_seen,
            seat_participation=state.seat_participation,
            timestamp=state.started_at,
        )
        self._db.record_hand(record)

    def on_parsed_hand(self, parsed_hand) -> None:
        """Called by LogTailer when a text-hand is completed."""
        participation = {}
        for action in parsed_hand.actions:
            # find seat by player_name
            seat_num = None
            for s, name in parsed_hand.seats.items():
                if name == action.player_name:
                    seat_num = s
                    break
            if seat_num is None:
                continue
            
            seat = f"seat_{seat_num}"
            if seat not in participation:
                participation[seat] = {
                    "player_name": action.player_name,
                    "action_bets": 0,
                    "action_calls": 0,
                    "action_raises": 0,
                    "preflop_raise": False,
                    "stayed_preflop": True,
                    "stayed_flop": False,
                    "stayed_turn": False,
                    "stayed_river": False,
                    "total_thinking_time": 0.0,
                    "turn_action_count": 0,
                }
            
            part = participation[seat]
            if action.action_type == "bet":
                part["action_bets"] += 1
            elif action.action_type == "call":
                part["action_calls"] += 1
            elif action.action_type == "raise":
                part["action_raises"] += 1
                if action.street == "preflop":
                    part["preflop_raise"] = True
            
            if action.street == "flop":
                part["stayed_flop"] = True
            elif action.street == "turn":
                part["stayed_turn"] = True
            elif action.street == "river":
                part["stayed_river"] = True

        record = HandRecord(
            session_id=self._db.session_id or 0,
            street_reached="unknown",
            board_cards=[], 
            seat_participation=participation,
            timestamp=time.time(),
        )
        self._db.record_hand(record)

    @property
    def seat_names(self) -> list[str]:
        return list(self._seats.keys())

    @property
    def current_street(self) -> str:
        return self._state.street if self._state else "preflop"

    @property
    def in_hand(self) -> bool:
        return self._state is not None
