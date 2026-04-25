"""
Equity calculator.

Strategy:
  - Pre-flop (no board): Use PreflopTable lookup (~0ms)
  - Post-flop (3-5 board cards): Monte Carlo with eval7 (~20-40ms for 5000 sims)

Falls back to treys if eval7 is not installed.
"""

import random
from dataclasses import dataclass
from typing import Optional

from src.common.constants import SPECIAL_LABELS, EQUITY_STRONG, EQUITY_MEDIUM, EQUITY_MARGINAL
from src.engine.lookup import PreflopTable


class DuplicateCardError(ValueError):
    """Raised when hero/board cards contain duplicates (CNN misread)."""

# Try fast C-backed evaluator first, fall back to treys
try:
    import eval7
    _BACKEND = "eval7"
except ImportError:
    try:
        from treys import Evaluator, Card as TreysCard, Deck as TreysDeck
        _BACKEND = "treys"
    except ImportError:
        _BACKEND = None


@dataclass
class EquityResult:
    equity: float               # Win probability in [0, 1]
    hand_strength: str          # "strong" / "medium" / "marginal" / "weak"
    street: str                 # "preflop" / "flop" / "turn" / "river"
    hand_class: Optional[str]   # e.g. "AKs", None for post-flop
    simulations: int            # 0 for lookup, N for Monte Carlo


def _classify_strength(equity: float) -> str:
    if equity >= EQUITY_STRONG:
        return "strong"
    elif equity >= EQUITY_MEDIUM:
        return "medium"
    elif equity >= EQUITY_MARGINAL:
        return "marginal"
    else:
        return "weak"


def _street_from_board(board: list[str]) -> str:
    n = sum(1 for c in board if c not in SPECIAL_LABELS)
    if n == 0:
        return "preflop"
    elif n == 3:
        return "flop"
    elif n == 4:
        return "turn"
    else:
        return "river"


def _run_simulation_loop(
    hero_cards,
    board_cards,
    deck: list,
    num_opponents: int,
    num_simulations: int,
    eval_hand_fn,
) -> float:
    """Core Monte Carlo loop shared by both backends. Returns equity in [0, 1].

    eval_hand_fn(hand, board) -> int, lower score is a better hand.
    """
    remaining_board = 5 - len(board_cards)
    wins = ties = 0

    for _ in range(num_simulations):
        sample = random.sample(deck, remaining_board + num_opponents * 2)
        run_board = board_cards + sample[:remaining_board]
        opp_hands = [
            sample[remaining_board + i * 2: remaining_board + i * 2 + 2]
            for i in range(num_opponents)
        ]
        hero_val = eval_hand_fn(hero_cards, run_board)
        best_opp = min(eval_hand_fn(h, run_board) for h in opp_hands)
        if hero_val < best_opp:
            wins += 1
        elif hero_val == best_opp:
            ties += 1

    return (wins + ties * 0.5) / num_simulations


# ---------------------------------------------------------------------------
# eval7 backend
# ---------------------------------------------------------------------------

def _monte_carlo_eval7(
    hero: list[str],
    board: list[str],
    num_opponents: int,
    num_simulations: int,
) -> float:
    """Run Monte Carlo equity simulation using eval7."""
    hero_cards = [eval7.Card(c) for c in hero]
    board_cards = [eval7.Card(c) for c in board if c not in SPECIAL_LABELS]

    known = set(hero_cards) | set(board_cards)
    deck = [c for c in eval7.Deck() if c not in known]

    # eval7: lower value = better hand
    return _run_simulation_loop(
        hero_cards, board_cards, deck, num_opponents, num_simulations,
        eval_hand_fn=lambda hand, run_board: eval7.evaluate(hand + run_board),
    )


# ---------------------------------------------------------------------------
# treys backend (fallback)
# ---------------------------------------------------------------------------

def _monte_carlo_treys(
    hero: list[str],
    board: list[str],
    num_opponents: int,
    num_simulations: int,
) -> float:
    from treys import Evaluator, Card as TreysCard
    evaluator = Evaluator()

    def to_treys(label: str) -> int:
        return TreysCard.new(label[0] + label[1])

    hero_cards = [to_treys(c) for c in hero]
    board_cards = [to_treys(c) for c in board if c not in SPECIAL_LABELS]
    known_set = set(hero_cards + board_cards)

    all_cards = [TreysCard.new(r + s) for r in "23456789TJQKA" for s in "cdhs"]
    deck = [c for c in all_cards if c not in known_set]

    # treys: lower = better
    return _run_simulation_loop(
        hero_cards, board_cards, deck, num_opponents, num_simulations,
        eval_hand_fn=lambda hand, run_board: evaluator.evaluate(run_board, hand),
    )


# ---------------------------------------------------------------------------
# Public interface
# ---------------------------------------------------------------------------

class EquityCalculator:
    """
    Calculates hero equity given hole cards, board, and opponent count.

    Uses pre-flop lookup for speed pre-flop, Monte Carlo post-flop.
    """

    def __init__(
        self,
        num_simulations: int = 5000,
        preflop_table_path: Optional[str] = None,
    ) -> None:
        self._num_simulations = num_simulations
        kwargs = {"table_path": preflop_table_path} if preflop_table_path else {}
        try:
            self._preflop = PreflopTable(**kwargs)
        except FileNotFoundError:
            self._preflop = None

        if _BACKEND is None:
            raise RuntimeError(
                "No hand evaluator found. Install eval7 or treys:\n"
                "  pip install eval7\n"
                "  pip install treys"
            )

    def calculate(
        self,
        hero: list[str],
        board: list[str],
        num_opponents: int = 1,
    ) -> Optional[EquityResult]:
        """
        Calculate equity.

        Args:
            hero:          List of 2 card labels (e.g. ['Ah', 'Kd']).
            board:         List of 0-5 card labels. 'empty'/'back'/'unknown' are ignored.
            num_opponents: Number of active opponents (1-9).

        Returns:
            EquityResult or None if hero cards are unknown/invalid.
        """
        if len(hero) != 2:
            return None
        if any(c in SPECIAL_LABELS for c in hero):
            return None

        num_opponents = max(1, min(9, num_opponents))
        street = _street_from_board(board)
        known_board = [c for c in board if c not in SPECIAL_LABELS]

        # Check for ML hallucinations (duplicate cards). Evaluators crash on duplicates.
        all_known = hero + known_board
        if len(set(all_known)) != len(all_known):
            raise DuplicateCardError(f"Duplicate cards detected: {all_known}")

        if street == "preflop":
            equity = self._preflop_equity(hero[0], hero[1], num_opponents)
            if equity is None:
                # Fallback to Monte Carlo if table not available
                equity = self._monte_carlo(hero, [], num_opponents)
                sims = self._num_simulations
            else:
                sims = 0
            hand_class = self._preflop.hand_class(hero[0], hero[1]) if self._preflop else None
        else:
            equity = self._monte_carlo(hero, known_board, num_opponents)
            sims = self._num_simulations
            hand_class = None

        return EquityResult(
            equity=round(equity, 4),
            hand_strength=_classify_strength(equity),
            street=street,
            hand_class=hand_class,
            simulations=sims,
        )

    def _preflop_equity(self, card1: str, card2: str, num_opponents: int) -> Optional[float]:
        if self._preflop is None:
            return None
        return self._preflop.get_equity(card1, card2, num_opponents)

    def _monte_carlo(self, hero: list[str], board: list[str], num_opponents: int) -> float:
        if _BACKEND == "eval7":
            return _monte_carlo_eval7(hero, board, num_opponents, self._num_simulations)
        else:
            return _monte_carlo_treys(hero, board, num_opponents, self._num_simulations)
