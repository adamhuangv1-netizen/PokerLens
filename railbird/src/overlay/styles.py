"""
QSS styles and color constants for the overlay.
"""

from src.common.constants import EQUITY_STRONG, EQUITY_MEDIUM, EQUITY_MARGINAL

# Semi-transparent black background (RGBA)
PANEL_BG_COLOR = "rgba(20, 20, 20, 185)"
PANEL_BORDER_RADIUS = "8px"

# Equity bar colors
COLOR_STRONG   = "#2ecc71"   # green
COLOR_MEDIUM   = "#f39c12"   # orange
COLOR_MARGINAL = "#e67e22"   # dark orange
COLOR_WEAK     = "#e74c3c"   # red
COLOR_UNKNOWN  = "#7f8c8d"   # grey

# Suit colors
SUIT_RED   = "#e74c3c"
SUIT_BLACK = "#ecf0f1"

# Font
FONT_FAMILY = "Consolas, 'Courier New', monospace"
FONT_SIZE_LARGE  = "15px"
FONT_SIZE_MEDIUM = "12px"
FONT_SIZE_SMALL  = "10px"

HUD_STYLESHEET = f"""
QWidget#hud_panel {{
    background-color: {PANEL_BG_COLOR};
    border-radius: {PANEL_BORDER_RADIUS};
}}
QLabel {{
    font-family: {FONT_FAMILY};
    color: #ecf0f1;
    background: transparent;
}}
QLabel#equity_label {{
    font-size: {FONT_SIZE_LARGE};
    font-weight: bold;
}}
QLabel#action_label {{
    font-size: {FONT_SIZE_MEDIUM};
    font-weight: bold;
}}
QLabel#rationale_label {{
    font-size: {FONT_SIZE_SMALL};
    color: #bdc3c7;
}}
QLabel#cards_label {{
    font-size: {FONT_SIZE_MEDIUM};
}}
QLabel#status_label {{
    font-size: {FONT_SIZE_SMALL};
    color: #7f8c8d;
}}
"""

SEAT_HUD_STYLESHEET = f"""
QLabel {{
    font-family: {FONT_FAMILY};
    font-size: {FONT_SIZE_SMALL};
    color: #ecf0f1;
    background-color: rgba(20, 20, 20, 160);
    border-radius: 4px;
    padding: 2px 4px;
}}
"""


def equity_color(equity: float) -> str:
    if equity >= EQUITY_STRONG:
        return COLOR_STRONG
    elif equity >= EQUITY_MEDIUM:
        return COLOR_MEDIUM
    elif equity >= EQUITY_MARGINAL:
        return COLOR_MARGINAL
    else:
        return COLOR_WEAK


def suit_color(suit: str) -> str:
    return SUIT_RED if suit in ("h", "d") else SUIT_BLACK
