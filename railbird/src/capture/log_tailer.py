"""
Tailer for live poker hand history files (e.g., PokerStars format).

Provides a `LogTailer` that watches a directory for new lines in `.txt` files
and emits parsed hand actions to be consumed by the Tracker.
"""

import os
import time
import re
import threading
from dataclasses import dataclass, field
from typing import Callable, Optional

@dataclass
class PlayerAction:
    player_name: str
    action_type: str  # 'fold', 'check', 'call', 'bet', 'raise'
    street: str       # 'preflop', 'flop', 'turn', 'river'

@dataclass
class ParsedHand:
    hand_id: str
    seats: dict[int, str] = field(default_factory=dict)  # seat_number -> player_name
    actions: list[PlayerAction] = field(default_factory=list)


class HandParser:
    """Parses standard hand history lines into a ParsedHand object."""
    def __init__(self):
        self.current_hand: Optional[ParsedHand] = None
        self.current_street = "preflop"
        
        # Regexes for a typical PokerStars-like format
        self.re_hand_start = re.compile(r"Hand #(\d+):")
        self.re_seat = re.compile(r"Seat (\d+):\s+(.+?)\s+\(")
        self.re_flop = re.compile(r"\*\*\* FLOP \*\*\*")
        self.re_turn = re.compile(r"\*\*\* TURN \*\*\*")
        self.re_river = re.compile(r"\*\*\* RIVER \*\*\*")
        self.re_summary = re.compile(r"\*\*\* SUMMARY \*\*\*")
        self.re_action = re.compile(r"^([^:]+):\s+(folds|checks|calls|bets|raises)")

    def parse_line(self, line: str) -> Optional[ParsedHand]:
        """
        Parses a single line. 
        Returns a ParsedHand when the hand finishes (SUMMARY reached), else None.
        """
        line = line.strip()
        if not line:
            return None

        # Start of new hand
        m = self.re_hand_start.search(line)
        if m:
            self.current_hand = ParsedHand(hand_id=m.group(1))
            self.current_street = "preflop"
            return None

        if not self.current_hand:
            return None

        # Seats
        m = self.re_seat.match(line)
        if m:
            seat_num = int(m.group(1))
            player_name = m.group(2).strip()
            self.current_hand.seats[seat_num] = player_name
            return None

        # Street changes
        if self.re_flop.search(line):
            self.current_street = "flop"
            return None
        if self.re_turn.search(line):
            self.current_street = "turn"
            return None
        if self.re_river.search(line):
            self.current_street = "river"
            return None
            
        # End of hand
        if self.re_summary.search(line):
            completed_hand = self.current_hand
            self.current_hand = None
            return completed_hand

        # Actions
        m = self.re_action.match(line)
        if m:
            player_name = m.group(1).strip()
            action_type = m.group(2).strip()
            # Standardize action verbs
            if action_type.endswith('s'):
                action_type = action_type[:-1] # folds -> fold
                
            self.current_hand.actions.append(
                PlayerAction(
                    player_name=player_name, 
                    action_type=action_type, 
                    street=self.current_street
                )
            )

        return None


class LogTailer:
    """Watches a directory for the latest hand history file and tails it."""
    def __init__(self, directory: str, on_hand_parsed: Callable[[ParsedHand], None]):
        self.directory = directory
        self.on_hand_parsed = on_hand_parsed
        self.parser = HandParser()
        self._running = False
        self._thread: Optional[threading.Thread] = None

    def start(self):
        self._running = True
        self._thread = threading.Thread(target=self._tail_loop, daemon=True)
        self._thread.start()

    def stop(self):
        self._running = False
        if self._thread:
            self._thread.join(timeout=1.0)

    def _get_latest_file(self) -> Optional[str]:
        if not os.path.exists(self.directory):
            return None
        
        files = [os.path.join(self.directory, f) for f in os.listdir(self.directory) 
                 if f.endswith(".txt")]
        if not files:
            return None
            
        return max(files, key=os.path.getmtime)

    def _tail_loop(self):
        current_file = None
        f = None

        while self._running:
            latest_file = self._get_latest_file()
            
            if latest_file and latest_file != current_file:
                if f:
                    f.close()
                current_file = latest_file
                f = open(current_file, "r", encoding="utf-8", errors="ignore")
                # Jump to end to only stream new live hands
                f.seek(0, os.SEEK_END)

            if f:
                line = f.readline()
                if line:
                    hand = self.parser.parse_line(line)
                    if hand:
                        self.on_hand_parsed(hand)
                else:
                    time.sleep(0.5)
            else:
                time.sleep(2.0)
                
        if f:
            f.close()
