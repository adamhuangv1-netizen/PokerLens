"""
SQLite persistence layer for hand history and opponent stats.

Schema:
  sessions(id, profile_name, started_at, ended_at)
  hands(id, session_id, street_reached, board_cards, timestamp)
  hand_seats(id, hand_id, seat, stayed_preflop, stayed_flop, stayed_turn, stayed_river)

Writes are batched and flushed on a timer or explicit flush() call.
"""

import atexit
import json
import os
import sqlite3
import time
import threading
from dataclasses import dataclass
from typing import Optional

_DEFAULT_DB_PATH = os.path.join(
    os.path.dirname(__file__), "..", "..", "data", "pokerlens.db"
)

_MAX_PENDING = 1000


@dataclass
class HandRecord:
    session_id: int
    street_reached: str          # "preflop", "flop", "turn", "river"
    board_cards: list[str]
    seat_participation: dict[str, dict]  # seat -> {stayed_preflop, stayed_flop, ...}
    timestamp: float = 0.0


class PokerDB:
    """
    Thread-safe SQLite database for hand history.

    Writes are buffered in memory and flushed periodically or on close.
    """

    def __init__(self, db_path: str = _DEFAULT_DB_PATH) -> None:
        os.makedirs(os.path.dirname(db_path) or ".", exist_ok=True)
        self._db_path = db_path
        self._lock = threading.Lock()
        self._pending: list[HandRecord] = []
        self._session_id: Optional[int] = None

        self._conn = sqlite3.connect(db_path, check_same_thread=False)
        self._conn.row_factory = sqlite3.Row
        self._create_schema()
        atexit.register(self.close)

    def _create_schema(self) -> None:
        with self._conn:
            self._conn.executescript("""
                CREATE TABLE IF NOT EXISTS sessions (
                    id          INTEGER PRIMARY KEY AUTOINCREMENT,
                    profile_name TEXT NOT NULL,
                    started_at  REAL NOT NULL,
                    ended_at    REAL
                );
                CREATE TABLE IF NOT EXISTS hands (
                    id              INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id      INTEGER NOT NULL REFERENCES sessions(id),
                    street_reached  TEXT NOT NULL,
                    board_cards     TEXT,
                    timestamp       REAL NOT NULL
                );
                CREATE TABLE IF NOT EXISTS hand_seats (
                    id              INTEGER PRIMARY KEY AUTOINCREMENT,
                    hand_id         INTEGER NOT NULL REFERENCES hands(id),
                    seat            TEXT NOT NULL,
                    player_name     TEXT,
                    stayed_preflop  INTEGER NOT NULL DEFAULT 0,
                    stayed_flop     INTEGER NOT NULL DEFAULT 0,
                    stayed_turn     INTEGER NOT NULL DEFAULT 0,
                    stayed_river    INTEGER NOT NULL DEFAULT 0,
                    action_bets     INTEGER NOT NULL DEFAULT 0,
                    action_calls    INTEGER NOT NULL DEFAULT 0,
                    action_raises   INTEGER NOT NULL DEFAULT 0,
                    preflop_raise   INTEGER NOT NULL DEFAULT 0,
                    total_thinking_time REAL NOT NULL DEFAULT 0.0,
                    turn_action_count INTEGER NOT NULL DEFAULT 0
                );
                CREATE INDEX IF NOT EXISTS idx_hand_seats_seat ON hand_seats(seat);
                CREATE INDEX IF NOT EXISTS idx_hands_session ON hands(session_id);
            """)

    def start_session(self, profile_name: str) -> int:
        with self._lock:
            cur = self._conn.execute(
                "INSERT INTO sessions (profile_name, started_at) VALUES (?, ?)",
                (profile_name, time.time())
            )
            self._conn.commit()
            self._session_id = cur.lastrowid
            return self._session_id

    def end_session(self) -> None:
        if self._session_id is None:
            return
        self.flush()
        with self._lock:
            self._conn.execute(
                "UPDATE sessions SET ended_at = ? WHERE id = ?",
                (time.time(), self._session_id)
            )
            self._conn.commit()

    @property
    def session_id(self) -> Optional[int]:
        return self._session_id

    def get_pending_count(self) -> int:
        with self._lock:
            return len(self._pending)

    def record_hand(self, record: HandRecord) -> None:
        """Queue a hand for writing. Non-blocking. Drops oldest record if buffer is full."""
        with self._lock:
            if len(self._pending) >= _MAX_PENDING:
                self._pending.pop(0)
            self._pending.append(record)

    def flush(self) -> None:
        """Write all pending hand records to the database."""
        with self._lock:
            if not self._pending:
                return
            to_write = list(self._pending)
            self._pending.clear()
            session_id = self._session_id

        if session_id is None:
            return

        with self._lock:
            with self._conn:
                for rec in to_write:
                    cur = self._conn.execute(
                        "INSERT INTO hands (session_id, street_reached, board_cards, timestamp) "
                        "VALUES (?, ?, ?, ?)",
                        (session_id, rec.street_reached,
                         json.dumps(rec.board_cards), rec.timestamp or time.time())
                    )
                    hand_id = cur.lastrowid
                    for seat, participation in rec.seat_participation.items():
                        self._conn.execute(
                            "INSERT INTO hand_seats "
                            "(hand_id, seat, player_name, stayed_preflop, stayed_flop, stayed_turn, stayed_river, action_bets, action_calls, action_raises, preflop_raise, total_thinking_time, turn_action_count) "
                            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                            (
                                hand_id, seat,
                                participation.get("player_name"),
                                int(participation.get("stayed_preflop", False)),
                                int(participation.get("stayed_flop", False)),
                                int(participation.get("stayed_turn", False)),
                                int(participation.get("stayed_river", False)),
                                int(participation.get("action_bets", 0)),
                                int(participation.get("action_calls", 0)),
                                int(participation.get("action_raises", 0)),
                                int(participation.get("preflop_raise", False)),
                                float(participation.get("total_thinking_time", 0.0)),
                                int(participation.get("turn_action_count", 0)),
                            )
                        )

    def get_seat_hands(self, seat: str, session_id: Optional[int] = None) -> list[dict]:
        """Return all hand_seats rows for a seat (optionally filtered by session)."""
        sid = session_id or self._session_id
        if sid is None:
            return []
        with self._lock:
            rows = self._conn.execute(
                """SELECT hs.* FROM hand_seats hs
                   JOIN hands h ON h.id = hs.hand_id
                   WHERE hs.seat = ? AND h.session_id = ?""",
                (seat, sid)
            ).fetchall()
        return [dict(r) for r in rows]

    def get_total_hands(self, session_id: Optional[int] = None) -> int:
        sid = session_id or self._session_id
        if sid is None:
            return 0
        with self._lock:
            row = self._conn.execute(
                "SELECT COUNT(*) FROM hands WHERE session_id = ?", (sid,)
            ).fetchone()
        return row[0] if row else 0

    def close(self) -> None:
        self.end_session()
        try:
            self._conn.close()
        except Exception:
            pass
