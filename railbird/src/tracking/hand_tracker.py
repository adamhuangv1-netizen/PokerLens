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

# Consecutive frames required before acting on a state change (~300ms at 10fps).
# Prevents single-frame CNN misclassifications from triggering phantom hand commits,
# sticky stayed_* flags, or double-counted thinking-time.
_DEBOUNCE_FRAMES = 3


@dataclass
class _HandState:
    """Mutable state for the current in-progress hand."""
    started_at: float = 0.0
    street: str = "preflop"
    max_board_count: int = 0  # ratchets up; prevents street regression on flicker
    board_seen: list[str] = field(default_factory=list)
    # seat -> {stayed_preflop, stayed_flop, stayed_turn, stayed_river,
    #          total_thinking_time, turn_action_count}
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
        # When True, vision _commit_hand skips DB writes — log is the source of truth.
        self._log_available = False

        # Debounce counters (C3, H1, H2)
        self._hero_present_frames: int = 0
        self._hero_absent_frames: int = 0
        self._seat_present_frames: dict[str, int] = {}
        self._pending_active_seat: Optional[str] = None
        self._pending_active_frames: int = 0

    @staticmethod
    def _parse_seats(seat_keys: list[str]) -> dict[str, list[str]]:
        """Group card keys by seat name. seat_1_card_1, seat_1_card_2 -> seat_1: [...]"""
        seats: dict[str, list[str]] = {}
        for key in seat_keys:
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

        hero_labels = list(result.hero_cards)
        board_raw = list(result.community_cards)
        board_count = _count_known_board(board_raw)
        has_hero = _has_hero_cards(hero_labels)
        board_labels = [label for label, _ in board_raw if label not in SPECIAL_LABELS]

        # --- Debounced hero present/absent counters (C3) ---
        if has_hero:
            self._hero_present_frames += 1
            self._hero_absent_frames = 0
        else:
            self._hero_absent_frames += 1
            self._hero_present_frames = 0

        # --- Hand boundary detection (debounced) ---

        # New hand: N consecutive "hero present" frames while no state is active.
        # Using == so this fires exactly once per onset, not every frame.
        if self._hero_present_frames == _DEBOUNCE_FRAMES and self._state is None:
            self._state = _HandState(started_at=time.time())
            for seat in self._seats:
                self._state.seat_participation[seat] = {
                    "stayed_preflop": True,  # assume in until we see otherwise
                    "stayed_flop": False,
                    "stayed_turn": False,
                    "stayed_river": False,
                    "total_thinking_time": 0.0,
                    "turn_action_count": 0,
                }
            self._seat_present_frames = {}

        # Hand ended: N consecutive "hero absent" frames.
        if self._hero_absent_frames == _DEBOUNCE_FRAMES and self._state is not None:
            self._commit_hand(self._state)
            self._state = None

        # Update street and seat participation
        if self._state is not None and has_hero:
            self._state.board_seen = board_labels
            # Ratchet board count: prevents street regression if board flickers
            self._state.max_board_count = max(board_count, self._state.max_board_count)
            self._state.street = _street_from_count(self._state.max_board_count)
            current_street = self._state.street

            # Debounced active-seat transition (H2): require N frames of same seat
            raw_active = None
            for key, (label, conf) in result.cards.items():
                if "_active" in key and label not in SPECIAL_LABELS:
                    raw_active = key.split("_active")[0]
                    break

            if raw_active == self._pending_active_seat:
                self._pending_active_frames += 1
            else:
                self._pending_active_seat = raw_active
                self._pending_active_frames = 1

            if self._pending_active_frames == _DEBOUNCE_FRAMES:
                confirmed_active = self._pending_active_seat
                if self._state.current_turn_seat != confirmed_active:
                    if self._state.current_turn_seat is not None:
                        duration = time.time() - self._state.turn_started_at
                        part = self._state.seat_participation.get(self._state.current_turn_seat)
                        if part is not None:
                            part["total_thinking_time"] += duration
                            part["turn_action_count"] += 1
                    self._state.current_turn_seat = confirmed_active
                    self._state.turn_started_at = time.time()

            # Debounced seat card visibility (H1): N consecutive frames to set stayed_*
            for seat, card_keys in self._seats.items():
                has_cards = any(
                    result.cards.get(k, ("empty", 0))[0] not in SPECIAL_LABELS
                    for k in card_keys
                )
                if has_cards:
                    self._seat_present_frames[seat] = self._seat_present_frames.get(seat, 0) + 1
                else:
                    self._seat_present_frames[seat] = 0

                if self._seat_present_frames.get(seat, 0) >= _DEBOUNCE_FRAMES:
                    part = self._state.seat_participation.get(seat)
                    if part is not None:
                        if current_street == "flop":
                            part["stayed_flop"] = True
                        elif current_street == "turn":
                            part["stayed_turn"] = True
                        elif current_street == "river":
                            part["stayed_river"] = True

    def _commit_hand(self, state: _HandState) -> None:
        """Write a completed hand record to the database (skipped when log is available)."""
        if self._log_available:
            return
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
        self._log_available = True
        participation = {}
        for action in parsed_hand.actions:
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
