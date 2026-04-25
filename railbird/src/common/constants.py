"""
Canonical card label definitions shared across the entire codebase.

54 classes: 52 playing cards + 'empty' (no card in slot) + 'back' (card face-down).

Label format: rank + suit, lowercase suit.
  Ranks: 2 3 4 5 6 7 8 9 T J Q K A
  Suits: c (clubs) d (diamonds) h (hearts) s (spades)
  Special: 'empty', 'back'
"""

RANKS = ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]
SUITS = ["c", "d", "h", "s"]

# 52 card labels in rank-major order, then special classes
CARD_LABELS: list[str] = [f"{r}{s}" for r in RANKS for s in SUITS] + ["empty", "back"]

# Total number of classes
NUM_CLASSES: int = len(CARD_LABELS)  # 54

LABEL_TO_IDX: dict[str, int] = {label: idx for idx, label in enumerate(CARD_LABELS)}
IDX_TO_LABEL: dict[int, str] = {idx: label for idx, label in enumerate(CARD_LABELS)}

# Human-readable display strings
RANK_DISPLAY = {
    "2": "2", "3": "3", "4": "4", "5": "5", "6": "6",
    "7": "7", "8": "8", "9": "9", "T": "10",
    "J": "J", "Q": "Q", "K": "K", "A": "A",
}
SUIT_DISPLAY = {"c": "♣", "d": "♦", "h": "♥", "s": "♠"}
SUIT_COLOR = {"c": "#000000", "d": "#cc0000", "h": "#cc0000", "s": "#000000"}


# Special/non-card labels indicating no card or unknown state
SPECIAL_LABELS: frozenset[str] = frozenset({"empty", "back", "unknown"})

# Labels that mean the seat is empty / folded (back = face-down, still in the hand)
FOLDED_LABELS: frozenset[str] = frozenset({"empty", "unknown"})

# Equity strength thresholds — shared by hand strength classification and HUD coloring
EQUITY_STRONG: float = 0.65
EQUITY_MEDIUM: float = 0.50
EQUITY_MARGINAL: float = 0.35

# Overlay bar height in pixels
OVERLAY_HEIGHT: int = 70

# Street names in order
STREETS: tuple[str, ...] = ("preflop", "flop", "turn", "river")


def label_to_display(label: str) -> str:
    """Convert label like 'Ah' to display string like 'A♥'."""
    if label in SPECIAL_LABELS:
        return label.capitalize()
    rank, suit = label[:-1], label[-1]
    return f"{RANK_DISPLAY[rank]}{SUIT_DISPLAY[suit]}"


def canonicalize_preflop(card1: str, card2: str) -> str:
    """
    Convert two hole cards to a canonical pre-flop hand class string.
    e.g. ('Ah', 'Kh') -> 'AKs', ('7c', '2d') -> '72o', ('Jc', 'Js') -> 'JJ'
    """
    rank_order = {r: i for i, r in enumerate(RANKS)}

    r1, s1 = card1[:-1], card1[-1]
    r2, s2 = card2[:-1], card2[-1]

    # Put higher rank first
    if rank_order[r1] < rank_order[r2]:
        r1, r2 = r2, r1
        s1, s2 = s2, s1

    if r1 == r2:
        return f"{r1}{r2}"  # Pocket pair, e.g. "AA"
    elif s1 == s2:
        return f"{r1}{r2}s"  # Suited, e.g. "AKs"
    else:
        return f"{r1}{r2}o"  # Offsuit, e.g. "AKo"
