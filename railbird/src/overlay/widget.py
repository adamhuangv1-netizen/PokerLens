"""
OverlayWindow — the transparent, always-on-top, click-through PyQt6 window.

Key window flags:
  FramelessWindowHint          — no title bar or border
  WindowStaysOnTopHint         — always above other windows
  WindowTransparentForInput    — click events pass through to the poker client
  WA_TranslucentBackground     — true window transparency (alpha channel)
"""

from typing import Optional

from PyQt6.QtCore import Qt, QTimer, pyqtSignal, pyqtSlot
from PyQt6.QtWidgets import QApplication, QVBoxLayout, QWidget, QLabel

from src.overlay.hud import HudPanel
from src.capture.cropper import TableProfile
from src.engine.equity import EquityResult
from src.engine.strategy import Advice


class OverlayWindow(QWidget):
    """
    Transparent overlay window displaying the HUD.

    Must run on the main GUI thread. Use update_display() (via signal or
    direct call from main thread) to refresh the content.
    """

    # Signal used to safely update from a worker thread
    display_update = pyqtSignal(list, list, object, object, float, bool, dict)

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

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addStretch(1)  # Push main HUD to the bottom
        
        self._hud = HudPanel(self)
        layout.addWidget(self._hud)
        
        # Create seat HUD boxes
        self._seat_huds = {}
        if self._profile:
            # We group cards by seat
            seat_coords = {}
            for seat_region in self._profile.seat_cards:
                seat_name = seat_region.key.rsplit("_card", 1)[0]
                seat_coords[seat_name] = (seat_region.x, seat_region.y)
                
            for seat_name, (sx, sy) in seat_coords.items():
                lbl = QLabel("", self)
                lbl.setObjectName("seat_hud")
                lbl.setStyleSheet("background-color: rgba(20, 25, 30, 200); color: white; padding: 4px; border-radius: 4px; font-size: 11px;")
                lbl.move(sx - 20, sy - 40)
                lbl.hide()
                self._seat_huds[seat_name] = lbl

        # Connect signal for thread-safe updates
        self.display_update.connect(self._on_display_update)

        self._visible = True

    @pyqtSlot(list, list, object, object, float, bool, dict)
    def _on_display_update(
        self,
        hero_labels: list,
        board_labels: list,
        equity_result,
        advice,
        latency_ms: float,
        waiting: bool,
        seat_stats: dict,
    ) -> None:
        self._hud.update_display(
            hero_labels=hero_labels,
            board_labels=board_labels,
            equity_result=equity_result,
            advice=advice,
            latency_ms=latency_ms,
            waiting=waiting,
        )
        
        # Update seat huds
        for seat_name, lbl in self._seat_huds.items():
            if seat_name in seat_stats and not waiting:
                stats = seat_stats[seat_name]
                color = "green" if stats.vpip > 0.4 else "red" if stats.af > 2.0 else "white"
                
                vpip_pct = int(stats.vpip * 100)
                pfr_pct = int(stats.pfr * 100)
                lbl.setText(f"<b>{stats.player_name}</b><br><span style='color:{color}'>VPIP: {vpip_pct}% | PFR: {pfr_pct}% | AF: {stats.af}</span>")
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
    ) -> None:
        """
        Update the HUD. Safe to call from any thread (uses Qt signal).
        """
        self.display_update.emit(
            hero_labels,
            board_labels,
            equity_result,
            advice,
            latency_ms or 0.0,
            waiting,
            seat_stats or {},
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
