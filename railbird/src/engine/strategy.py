"""
Strategy advisor — converts equity into actionable recommendations.

In v1, advice is based solely on equity thresholds. Pot odds will be
incorporated once OCR for bet/pot amounts is added.
"""

from dataclasses import dataclass
from typing import Optional

from src.engine.equity import EquityResult


@dataclass
class Advice:
    action: str         # "Raise", "Call", "Check/Call", "Fold"
    rationale: str      # Short explanation
    equity_pct: int     # Rounded equity percentage for display


def advise(result: EquityResult, pot_odds: Optional[float] = None) -> Advice:
    """
    Generate a strategic recommendation from an EquityResult.

    Args:
        result:    EquityResult from EquityCalculator.
        pot_odds:  If known: the fraction of the pot you must call to stay in
                   (call_amount / (pot + call_amount)). E.g. calling $20 into
                   a $60 pot gives pot_odds = 20 / 80 = 0.25. If equity >
                   pot_odds, the call is +EV.

    Returns:
        Advice with action, rationale, and integer equity percentage.
    """
    eq = result.equity
    pct = round(eq * 100)
    street = result.street
    hand_class = result.hand_class or ""

    # Pot odds override if we have them
    if pot_odds is not None and 0 < pot_odds < 1:
        if eq > pot_odds:
            return Advice(
                action="Call / Raise",
                rationale=f"+EV: equity {pct}% > pot odds {round(pot_odds*100)}%",
                equity_pct=pct,
            )
        else:
            return Advice(
                action="Fold",
                rationale=f"-EV: equity {pct}% < pot odds {round(pot_odds*100)}%",
                equity_pct=pct,
            )

    # Equity-only thresholds
    if eq >= 0.70:
        action = "Raise"
        rationale = f"Strong hand ({pct}% equity)"
        if hand_class:
            rationale = f"{hand_class} — {rationale}"
    elif eq >= 0.55:
        action = "Call"
        rationale = f"Decent equity ({pct}%) — call or bet for value"
    elif eq >= 0.40:
        action = "Check/Call"
        rationale = f"Marginal ({pct}%) — need good pot odds to continue"
    elif eq >= 0.25:
        action = "Fold"
        rationale = f"Weak ({pct}%) — consider folding unless pot odds are good"
    else:
        action = "Fold"
        rationale = f"Very weak ({pct}%) — fold"

    # Pre-flop nuance: tighten up in early position (not tracked yet, simple note)
    if street == "preflop" and eq < 0.45:
        rationale += " (especially from early position)"

    return Advice(action=action, rationale=rationale, equity_pct=pct)
