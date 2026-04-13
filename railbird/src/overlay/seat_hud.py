"""
Per-seat HUD labels displayed near each opponent seat on the overlay.

Shows VPIP/PFR/AF stats for tracked opponents.
"""

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLabel, QWidget

from src.overlay.styles import SEAT_HUD_STYLESHEET
from src.tracking.stats import SeatStats


class SeatHudLabel(QLabel):
    """A small label positioned near a seat showing stats."""

    def __init__(self, seat: str, parent: QWidget = None) -> None:
        super().__init__(parent)
        self._seat = seat
        self.setObjectName(f"seat_hud_{seat}")
        self.setStyleSheet(SEAT_HUD_STYLESHEET)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._show_waiting()

    def _show_waiting(self) -> None:
        self.setText(f"{self._seat}\n—/—/—")

    def update_stats(self, stats: SeatStats) -> None:
        if stats.hands_played < 5:
            label = f"{self._seat}\n({stats.hands_played}h)"
        else:
            vpip = round(stats.vpip * 100)
            pfr = round(stats.pfr * 100)
            af = round(stats.af, 1)
            label = f"{self._seat}\n{vpip}/{pfr}/{af}"
        self.setText(label)

    def clear_stats(self) -> None:
        self._show_waiting()
