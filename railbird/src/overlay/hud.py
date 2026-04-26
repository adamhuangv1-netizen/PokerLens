"""
HUD panel — vertical info panel shown on the right side of the overlay.
"""

from typing import Optional

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QProgressBar, QVBoxLayout, QWidget, QFrame

from src.engine.equity import EquityResult
from src.engine.strategy import Advice
from src.overlay.styles import equity_color, suit_color
from src.common.constants import label_to_display


_STREET = {0: "PREFLOP", 3: "FLOP", 4: "TURN", 5: "RIVER"}

_ACTION_BG = {
    "RAISE": "#1a7a3a",
    "BET":   "#1a7a3a",
    "CALL":  "#7a5a00",
    "CHECK": "#1a3a6a",
    "FOLD":  "#6a1a1a",
}
_ACTION_BORDER = {
    "RAISE": "#2ecc71",
    "BET":   "#2ecc71",
    "CALL":  "#f39c12",
    "CHECK": "#3498db",
    "FOLD":  "#e74c3c",
}


def _card_html(label: str, size: str = "13px") -> str:
    if label in ("unknown", "empty", "back", ""):
        return f'<span style="color:#7f8c8d;font-size:{size}">?</span>'
    display = label_to_display(label)
    color = suit_color(label[-1] if label else "")
    return f'<span style="color:{color};font-size:{size}">{display}</span>'


def _row_label(text: str) -> QLabel:
    lbl = QLabel(text)
    lbl.setStyleSheet("color: #7f8c8d; font-size: 9px; font-family: Consolas; letter-spacing: 1px;")
    return lbl


def _row_value() -> QLabel:
    lbl = QLabel("—")
    lbl.setStyleSheet("color: #ecf0f1; font-size: 12px; font-family: Consolas;")
    lbl.setAlignment(Qt.AlignmentFlag.AlignRight)
    return lbl


def _divider() -> QFrame:
    line = QFrame()
    line.setFrameShape(QFrame.Shape.HLine)
    line.setStyleSheet("color: #2c3e50;")
    return line


class HudPanel(QWidget):
    """Vertical HUD panel: header, info rows, equity, action box."""

    PANEL_W = 220

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("hud_panel")
        self.setFixedWidth(self.PANEL_W)
        self.setStyleSheet("""
            QWidget#hud_panel {
                background-color: rgba(10, 14, 20, 230);
                border-radius: 8px;
            }
            QLabel { background: transparent; }
        """)
        self._build_ui()

    def _build_ui(self) -> None:
        root = QVBoxLayout(self)
        root.setContentsMargins(12, 10, 12, 10)
        root.setSpacing(0)

        # --- Header ---
        self._header = QLabel("POKERLENS  ·  PREFLOP")
        self._header.setStyleSheet(
            "color: #ecf0f1; font-size: 10px; font-family: Consolas; letter-spacing: 1px;"
        )
        live_row = QHBoxLayout()
        live_row.setContentsMargins(0, 0, 0, 0)
        live_row.addWidget(self._header)
        live_row.addStretch()
        self._live_dot = QLabel("● LIVE")
        self._live_dot.setStyleSheet("color: #2ecc71; font-size: 9px; font-family: Consolas;")
        live_row.addWidget(self._live_dot)
        root.addLayout(live_row)
        root.addSpacing(8)
        root.addWidget(_divider())
        root.addSpacing(8)

        # --- Info rows ---
        def _info_row(key_text):
            row = QHBoxLayout()
            row.setContentsMargins(0, 2, 0, 2)
            key = _row_label(key_text)
            val = _row_value()
            row.addWidget(key)
            row.addStretch()
            row.addWidget(val)
            return row, val

        hero_row, self._hero_val = _info_row("HERO")
        board_row, self._board_val = _info_row("BOARD")
        pot_row, self._pot_val = _info_row("POT / CALL")
        odds_row, self._odds_val = _info_row("POT ODDS")

        root.addLayout(hero_row)
        root.addLayout(board_row)
        root.addSpacing(4)
        root.addWidget(_divider())
        root.addSpacing(4)
        root.addLayout(pot_row)
        root.addLayout(odds_row)
        root.addSpacing(8)
        root.addWidget(_divider())
        root.addSpacing(8)

        # --- Equity section ---
        self._opp_label = QLabel("EQUITY VS — OPPONENTS")
        self._opp_label.setStyleSheet(
            "color: #7f8c8d; font-size: 9px; font-family: Consolas; letter-spacing: 1px;"
        )
        root.addWidget(self._opp_label)
        root.addSpacing(4)

        # Big equity number
        self._equity_label = QLabel("—")
        self._equity_label.setStyleSheet(
            "color: #2ecc71; font-size: 42px; font-weight: bold; font-family: Consolas;"
        )
        self._equity_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        root.addWidget(self._equity_label)

        # Progress bar
        self._equity_bar = QProgressBar()
        self._equity_bar.setRange(0, 100)
        self._equity_bar.setValue(0)
        self._equity_bar.setTextVisible(False)
        self._equity_bar.setFixedHeight(5)
        self._equity_bar.setStyleSheet("""
            QProgressBar { background-color: #1a2030; border-radius: 2px; border: none; }
            QProgressBar::chunk { background-color: #2ecc71; border-radius: 2px; }
        """)
        root.addWidget(self._equity_bar)
        root.addSpacing(10)

        # --- Action box ---
        self._action_box = QWidget()
        self._action_box.setObjectName("action_box")
        self._action_box.setStyleSheet(
            "QWidget#action_box { background-color: #1a7a3a; border-radius: 6px; border: 1px solid #2ecc71; }"
        )
        action_layout = QVBoxLayout(self._action_box)
        action_layout.setContentsMargins(10, 8, 10, 8)
        action_layout.setSpacing(2)

        action_top = QHBoxLayout()
        self._action_badge = QLabel("RAISE")
        self._action_badge.setStyleSheet(
            "color: #ffffff; font-size: 13px; font-weight: bold; font-family: Consolas;"
        )
        self._action_ev = QLabel("+EV")
        self._action_ev.setStyleSheet(
            "color: #2ecc71; font-size: 11px; font-family: Consolas;"
        )
        action_top.addWidget(self._action_badge)
        action_top.addStretch()
        action_top.addWidget(self._action_ev)
        action_layout.addLayout(action_top)

        self._action_detail = QLabel("—")
        self._action_detail.setStyleSheet(
            "color: #bdc3c7; font-size: 10px; font-family: Consolas;"
        )
        self._action_detail.setWordWrap(True)
        action_layout.addWidget(self._action_detail)

        root.addWidget(self._action_box)
        root.addStretch()

        # Latency (hidden by default)
        self._status_label = QLabel("")
        self._status_label.setStyleSheet("color: #4a5568; font-size: 9px; font-family: Consolas;")
        self._status_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        root.addWidget(self._status_label)

    # ------------------------------------------------------------------

    def update_display(
        self,
        hero_labels: list[str],
        board_labels: list[str],
        equity_result: Optional[EquityResult],
        advice: Optional[Advice],
        latency_ms: Optional[float] = None,
        waiting: bool = False,
        error_message: Optional[str] = None,
        pot_amount: Optional[float] = None,
        to_call_amount: Optional[float] = None,
        num_opponents: int = 1,
    ) -> None:
        # Street
        known_board = [c for c in board_labels if c not in ("unknown", "empty", "back")]
        street = _STREET.get(len(known_board), "PREFLOP")
        self._header.setText(f"POKERLENS  ·  {street}")

        if error_message:
            self._hero_val.setText(f'<span style="color:#e74c3c">error</span>')
            self._hero_val.setTextFormat(Qt.TextFormat.RichText)
            self._action_badge.setText("ERR")
            self._action_detail.setText(error_message)
            return

        if waiting or not hero_labels or all(l in ("unknown", "empty") for l in hero_labels):
            self._hero_val.setText("—")
            self._board_val.setText("—")
            self._pot_val.setText("—")
            self._odds_val.setText("—")
            self._equity_label.setText("—")
            self._equity_bar.setValue(0)
            self._opp_label.setText("EQUITY VS — OPPONENTS")
            self._action_badge.setText("—")
            self._action_detail.setText("Waiting for hand...")
            self._live_dot.setStyleSheet("color: #7f8c8d; font-size: 9px; font-family: Consolas;")
            return

        self._live_dot.setStyleSheet("color: #2ecc71; font-size: 9px; font-family: Consolas;")

        # Hero
        hero_html = " ".join(_card_html(c) for c in hero_labels if c not in ("unknown", "empty"))
        self._hero_val.setText(hero_html)
        self._hero_val.setTextFormat(Qt.TextFormat.RichText)

        # Board
        if known_board:
            board_html = " ".join(_card_html(c) for c in known_board)
        else:
            board_html = "—"
        self._board_val.setText(board_html)
        self._board_val.setTextFormat(Qt.TextFormat.RichText)

        # Pot / Call
        if pot_amount is not None and to_call_amount is not None:
            self._pot_val.setText(f"${pot_amount:.0f} / ${to_call_amount:.0f}")
        elif pot_amount is not None:
            self._pot_val.setText(f"${pot_amount:.0f}")
        else:
            self._pot_val.setText("—")

        # Pot odds
        if pot_amount and to_call_amount and to_call_amount > 0:
            odds_pct = to_call_amount / (pot_amount + to_call_amount) * 100
            self._odds_val.setText(f"{odds_pct:.1f}%")
        else:
            self._odds_val.setText("—")

        # Equity
        self._opp_label.setText(f"EQUITY VS {num_opponents} OPPONENT{'S' if num_opponents != 1 else ''}")
        if equity_result is not None:
            pct = equity_result.equity * 100
            color = equity_color(equity_result.equity)
            # Split into integer and decimal parts
            int_part = int(pct)
            dec_part = round((pct - int_part) * 10)
            self._equity_label.setText(
                f'<span style="font-size:42px">{int_part}</span>'
                f'<span style="font-size:20px">.{dec_part}%</span>'
            )
            self._equity_label.setTextFormat(Qt.TextFormat.RichText)
            self._equity_label.setStyleSheet(
                f"color: {color}; font-weight: bold; font-family: Consolas;"
            )
            self._equity_bar.setValue(int(pct))
            self._equity_bar.setStyleSheet(f"""
                QProgressBar {{ background-color: #1a2030; border-radius: 2px; border: none; }}
                QProgressBar::chunk {{ background-color: {color}; border-radius: 2px; }}
            """)
        else:
            self._equity_label.setText("—")
            self._equity_bar.setValue(0)

        # Action
        if advice is not None:
            action = advice.action.upper()
            bg = _ACTION_BG.get(action, "#1a3a6a")
            border = _ACTION_BORDER.get(action, "#3498db")
            self._action_box.setStyleSheet(
                f"QWidget#action_box {{ background-color: {bg}; border-radius: 6px; border: 1px solid {border}; }}"
            )
            self._action_badge.setText(action)
            # EV indicator
            rationale = advice.rationale or ""
            if "+EV" in rationale or "edge" in rationale.lower():
                self._action_ev.setText("+EV")
                self._action_ev.setStyleSheet(f"color: {border}; font-size: 11px; font-family: Consolas;")
            else:
                self._action_ev.setText("")
            self._action_detail.setText(rationale)
        else:
            self._action_badge.setText("—")
            self._action_ev.setText("")
            self._action_detail.setText("")

        # Latency
        self._status_label.setText(f"{latency_ms:.0f}ms" if latency_ms is not None else "")
