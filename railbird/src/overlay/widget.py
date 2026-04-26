"""
OverlayWindow — the transparent, always-on-top, click-through PyQt6 window.

Key window flags:
  FramelessWindowHint          — no title bar or border
  WindowStaysOnTopHint         — always above other windows
  WindowTransparentForInput    — click events pass through to the poker client
  WA_TranslucentBackground     — true window transparency (alpha channel)
"""

from typing import Optional

from PyQt6.QtCore import Qt, pyqtSignal, pyqtSlot
from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget, QLabel

from src.overlay.hud import HudPanel
from src.overlay.styles import COLOR_STRONG, COLOR_MEDIUM, COLOR_WEAK, COLOR_UNKNOWN
from src.capture.cropper import TableProfile
from src.engine.equity import EquityResult
from src.engine.strategy import Advice


class OverlayWindow(QWidget):
    """
    Transparent overlay window displaying the HUD.

    Must run on the main GUI thread. Use update_display() (via signal or
    direct call from main thread) to refresh the content.
    """

    # Signal used to safely update from a worker thread (11-tuple)
    display_update = pyqtSignal(list, list, object, object, float, bool, dict, object, object, object, int)

    def __init__(
        self,
        x: int = 0,
        y: int = 0,
        width: int = 600,
        height: int = 70,
        profile: Optional[TableProfile] = None,
        parent=None,
    ) -> None:
        super().__init__(parent)
        self._profile = profile

        # Window flags for transparent click-through overlay
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.WindowTransparentForInput
            | Qt.WindowType.Tool  # Keeps it off the taskbar
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.setGeometry(x, y, width, height)

        # HUD panel anchored to the right side of the overlay
        outer = QHBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.addStretch(1)

        right_col = QVBoxLayout()
        right_col.setContentsMargins(0, 0, 0, 0)
        self._hud = HudPanel(self)
        right_col.addWidget(self._hud)
        right_col.addStretch(1)
        outer.addLayout(right_col)
        
        # Create seat HUD boxes, positioned using percentage coords relative to overlay size
        self._seat_huds = {}
        if self._profile:
            seat_coords: dict[str, tuple[int, int]] = {}
            for seat_region in self._profile.seat_cards:
                seat_name = seat_region.key.rsplit("_card", 1)[0]
                if seat_name not in seat_coords:
                    px, py, _, _ = seat_region.to_pixels(width, height)
                    seat_coords[seat_name] = (px, py)

            for seat_name, (sx, sy) in seat_coords.items():
                lbl = QLabel("", self)
                lbl.setObjectName("seat_hud")
                lbl.setStyleSheet("background-color: rgba(20, 25, 30, 200); color: white; "
                                  "padding: 4px; border-radius: 4px; font-size: 11px;")
                lbl.move(max(0, sx - 20), max(0, sy - 40))
                lbl.hide()
                self._seat_huds[seat_name] = lbl

        # Connect signal for thread-safe updates
        self.display_update.connect(self._on_display_update)

        self._visible = True

    _ARCHETYPE_COLOR = {
        "TAG": "white", "Nit": "#5dade2", "LAG": COLOR_MEDIUM, "LAG-light": "#f0b27a",
        "Maniac": COLOR_WEAK, "Fish": COLOR_STRONG, "Loose-Passive": "#a569bd", "Reg": "white",
        "Unknown": COLOR_UNKNOWN,
    }

    @pyqtSlot(list, list, object, object, float, bool, dict, object, object, object, int)
    def _on_display_update(
        self,
        hero_labels: list,
        board_labels: list,
        equity_result,
        advice,
        latency_ms: float,
        waiting: bool,
        seat_stats: dict,
        error_message,
        pot_amount,
        to_call_amount,
        num_opponents: int,
    ) -> None:
        self._hud.update_display(
            hero_labels=hero_labels,
            board_labels=board_labels,
            equity_result=equity_result,
            advice=advice,
            latency_ms=latency_ms,
            waiting=waiting,
            error_message=error_message,
            pot_amount=pot_amount,
            to_call_amount=to_call_amount,
            num_opponents=num_opponents,
        )

        for seat_name, lbl in self._seat_huds.items():
            if seat_name in seat_stats and not waiting:
                stats = seat_stats[seat_name]
                archetype = getattr(stats, "player_type", "Unknown")
                color = self._ARCHETYPE_COLOR.get(archetype, "white")
                vpip_pct = int(stats.vpip * 100)
                pfr_pct = int(stats.pfr * 100)
                lbl.setText(
                    f"<b>{stats.player_name}</b> "
                    f"<span style='color:{color}'>[{archetype}]</span><br>"
                    f"<span style='color:{color}'>VPIP: {vpip_pct}% | PFR: {pfr_pct}% | AF: {stats.af}</span>"
                )
                lbl.setTextFormat(Qt.TextFormat.RichText)
                lbl.adjustSize()
                lbl.show()
                lbl.raise_()
            else:
                lbl.hide()

    def update_display(
        self,
        hero_labels: list[str],
        board_labels: list[str],
        equity_result: Optional[EquityResult] = None,
        advice: Optional[Advice] = None,
        latency_ms: Optional[float] = None,
        waiting: bool = False,
        seat_stats: Optional[dict] = None,
        error_message: Optional[str] = None,
        pot_amount: Optional[float] = None,
        to_call_amount: Optional[float] = None,
        num_opponents: int = 1,
    ) -> None:
        """Update the HUD. Safe to call from any thread (uses Qt signal)."""
        self.display_update.emit(
            hero_labels,
            board_labels,
            equity_result,
            advice,
            latency_ms or 0.0,
            waiting,
            seat_stats or {},
            error_message,
            pot_amount,
            to_call_amount,
            num_opponents,
        )

    def reposition(self, x: int, y: int, width: int, height: int) -> None:
        """Move and resize the overlay window."""
        self.setGeometry(x, y, width, height)

    def toggle_visible(self) -> None:
        if self._visible:
            self.hide()
        else:
            self.show()
        self._visible = not self._visible
