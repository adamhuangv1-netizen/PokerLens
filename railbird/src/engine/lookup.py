"""
Pre-flop equity lookup table.

Maps the 169 canonical starting hand classes to equity vs 1-9 opponents.
The table is generated once by scripts/generate_preflop_table.py and stored
as data/preflop_equity.json.

Format:
{
    "AAs":  [0.852, 0.730, 0.636, ...],   // equity vs 1,2,3,...9 opponents
    "AKs":  [0.674, 0.543, ...],
    ...
    "72o":  [0.355, 0.245, ...]
}
"""

import json
import os
from typing import Optional

from src.common.constants import canonicalize_preflop

_DEFAULT_TABLE_PATH = os.path.join(
    os.path.dirname(__file__), "..", "..", "data", "preflop_equity.json"
)


class PreflopTable:
    """Fast pre-flop equity lookup by hand class and opponent count."""

    def __init__(self, table_path: str = _DEFAULT_TABLE_PATH) -> None:
        if not os.path.exists(table_path):
            raise FileNotFoundError(
                f"Pre-flop equity table not found at {table_path}.\n"
                "Run: python scripts/generate_preflop_table.py"
            )
        with open(table_path) as f:
            self._table: dict[str, list[float]] = json.load(f)

    def get_equity(self, card1: str, card2: str, num_opponents: int) -> Optional[float]:
        """
        Look up pre-flop equity for hole cards against num_opponents random hands.

        Args:
            card1, card2: Card labels like 'Ah', 'Kd'. Must not be 'empty'/'back'/'unknown'.
            num_opponents: 1-9.

        Returns:
            Equity as a float in [0, 1], or None if the hand can't be looked up.
        """
        if card1 in ("empty", "back", "unknown") or card2 in ("empty", "back", "unknown"):
            return None

        hand_class = canonicalize_preflop(card1, card2)
        row = self._table.get(hand_class)
        if row is None:
            return None

        idx = max(0, min(num_opponents - 1, len(row) - 1))
        return row[idx]

    def hand_class(self, card1: str, card2: str) -> Optional[str]:
        """Return canonical hand class string, e.g. 'AKs', 'TT', '72o'."""
        if card1 in ("empty", "back", "unknown") or card2 in ("empty", "back", "unknown"):
            return None
        return canonicalize_preflop(card1, card2)
