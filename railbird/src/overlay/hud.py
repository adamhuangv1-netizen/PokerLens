"""
HUD panel — the main info display shown on the overlay.

Shows:
  - Hero hole cards
  - Community cards
  - Equity percentage + color bar
  - Hand strength label
  - Recommended action + rationale
  - Pipeline latency (debug, toggleable)
"""

from typing import Optional

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QProgressBar, QVBoxLayout, QWidget

from src.engine.equity import EquityResult
from src.engine.strategy import Advice
from src.overlay.styles import (
    HUD_STYLESHEET,
    equity_color,
    suit_color,
    COLOR_UNKNOWN,
)
from src.common.constants import label_to_display


def _card_html(label: str) -> str:
    """Format a card label as colored HTML text."""
    if label in ("unknown", "empty", "back", ""):
        return f'<span style="color:#7f8c8d">?</span>'
    display = label_to_display(label)
    suit = label[-1] if len(label) >= 1 else ""
    color = suit_color(suit)
    return f'<span style="color:{color}">{display}</span>'


class HudPanel(QWidget):
    """
    Compact HUD bar showing equity and strategic advice.
    Designed to be placed at the top or bottom of the overlay window.
    """

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("hud_panel")
        self.setStyleSheet(HUD_STYLESHEET)
        self._build_ui()

    def _build_ui(self) -> None:
        root = QHBoxLayout(self)
        root.setContentsMargins(10, 6, 10, 6)
        root.setSpacing(12)

        # Cards column
        cards_col = QVBoxLayout()
        self._cards_label = QLabel("? ?")
        self._cards_label.setObjectName("cards_label")
        self._board_label = QLabel("Board: —")
        self._board_label.setObjectName("cards_label")
        cards_col.addWidget(self._cards_label)
        cards_col.addWidget(self._board_label)
        root.addLayout(cards_col)

        # Equity column
        eq_col = QVBoxLayout()
        self._equity_label = QLabel("—%")
        self._equity_label.setObjectName("equity_label")
        self._equity_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._equity_bar = QProgressBar()
        self._equity_bar.setRange(0, 100)
        self._equity_bar.setValue(0)
        self._equity_bar.setTextVisible(False)
        self._equity_bar.setFixedHeight(6)
        self._equity_bar.setFixedWidth(80)
        eq_col.addWidget(self._equity_label)
        eq_col.addWidget(self._equity_bar)
        root.addLayout(eq_col)

        # Action column
        action_col = QVBoxLayout()
        self._action_label = QLabel("—")
        self._action_label.setObjectName("action_label")
        self._rationale_label = QLabel("")
        self._rationale_label.setObjectName("rationale_label")
        self._rationale_label.setWordWrap(True)
        action_col.addWidget(self._action_label)
        action_col.addWidget(self._rationale_label)
        root.addLayout(action_col, stretch=1)

        # Status / latency
        self._status_label = QLabel("")
        self._status_label.setObjectName("status_label")
        self._status_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignBottom)
        root.addWidget(self._status_label)

    def update_display(
        self,
        hero_labels: list[str],
        board_labels: list[str],
        equity_result: Optional[EquityResult],
        advice: Optional[Advice],
        latency_ms: Optional[float] = None,
        waiting: bool = False,
        error_message: Optional[str] = None,
    ) -> None:
        """Update all HUD elements. Call from the main GUI thread only."""

        if error_message:
            self._cards_label.setText("Recognition error")
            self._board_label.setText("")
            self._equity_label.setText("—%")
            self._equity_bar.setValue(0)
            self._equity_bar.setStyleSheet("")
            self._action_label.setText("—")
            self._rationale_label.setText(
                f'<span style="color:#e74c3c">{error_message}</span>'
            )
            self._rationale_label.setTextFormat(Qt.TextFormat.RichText)
            return

        if waiting or not hero_labels or all(l in ("unknown", "empty") for l in hero_labels):
            self._cards_label.setText("Waiting for hand...")
            self._board_label.setText("")
            self._equity_label.setText("—%")
            self._equity_bar.setValue(0)
            self._equity_bar.setStyleSheet("")
            self._action_label.setText("—")
            self._rationale_label.setText("")
            return

        # Hero cards
        hero_html = " ".join(_card_html(c) for c in hero_labels)
        self._cards_label.setText(hero_html)
        self._cards_label.setTextFormat(Qt.TextFormat.RichText)

        # Board
        known_board = [c for c in board_labels if c not in ("unknown", "empty", "back")]
        if known_board:
            board_html = "Board: " + " ".join(_card_html(c) for c in known_board)
        else:
            board_html = "Board: —"
        self._board_label.setText(board_html)
        self._board_label.setTextFormat(Qt.TextFormat.RichText)

        # Equity
        if equity_result is not None:
            pct = round(equity_result.equity * 100)
            color = equity_color(equity_result.equity)
            self._equity_label.setText(f"{pct}%")
            self._equity_label.setStyleSheet(f"color: {color}; font-size: 15px; font-weight: bold;")
            self._equity_bar.setValue(pct)
            self._equity_bar.setStyleSheet(
                f"QProgressBar::chunk {{ background-color: {color}; border-radius: 3px; }}"
            )
        else:
            self._equity_label.setText("—%")
            self._equity_label.setStyleSheet(f"color: {COLOR_UNKNOWN};")
            self._equity_bar.setValue(0)

        # Action
        if advice is not None:
            self._action_label.setText(advice.action)
            self._rationale_label.setText(advice.rationale)
        else:
            self._action_label.setText("—")
            self._rationale_label.setText("")

        # Latency
        if latency_ms is not None:
            self._status_label.setText(f"{latency_ms:.0f}ms")
        else:
            self._status_label.setText("")
