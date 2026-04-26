"""
CalibratorOverlay — live, transparent PyQt6 calibration tool.

Draws rectangles directly on top of the poker window (no separate screenshot
window). The overlay covers the poker window area; you see the real table
through it while dragging region boxes.

Controls:
    Drag left mouse button — draw region
    Enter / Space          — confirm current region and advance
    S                      — skip (optional regions only)
    Backspace              — undo previous region and go back one step
    R                      — clear current rectangle without going back
    Esc                    — abort calibration

Usage (via scripts/calibrate.py):
    python scripts/calibrate.py --window "PokerStars" --profile-name "ps_6max"
"""

import os
import sys
from typing import Optional

from PyQt6.QtCore import Qt, QRect, QPoint, pyqtSignal
from PyQt6.QtGui import QPainter, QColor, QPen, QBrush, QFont
from PyQt6.QtWidgets import QApplication, QWidget

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from src.capture.cropper import RegionDef, TableProfile, save_profile
from src.capture.window import find_window


_REGION_SEQUENCE: list[tuple[str, str, Optional[str], bool]] = [
    ("hero_1",          "Hero Card 1",                      None, False),
    ("hero_2",          "Hero Card 2",                      None, False),
    ("flop_1",          "Community: Flop 1",                None, False),
    ("flop_2",          "Community: Flop 2",                None, False),
    ("flop_3",          "Community: Flop 3",                None, False),
    ("turn",            "Community: Turn",                  None, False),
    ("river",           "Community: River",                 None, False),
    ("pot_region",      "Pot total (S=skip if no OCR)",     None, True),
    ("to_call_region",  "To-call amount (S=skip if no OCR)", None, True),
]

_SEAT_SEQUENCE: list[tuple[str, str, Optional[str], bool]] = [
    (f"seat_{s}_card_{c}", f"Seat {s} Card {c}", f"seat_{s}", False)
    for s in range(1, 6)
    for c in range(1, 3)
]


def _pct(val: int, total: int) -> float:
    return val / total if total > 0 else 0.0


class CalibratorOverlay(QWidget):
    """
    Translucent, interactive overlay for region selection.

    Emits `done` with a list[RegionDef] on completion, or None on abort.
    """

    done = pyqtSignal(object)

    def __init__(
        self,
        x: int, y: int, w: int, h: int,
        sequence: list[tuple[str, str, Optional[str], bool]],
    ) -> None:
        super().__init__()
        self._sequence = sequence
        self._regions: list[RegionDef] = []
        self._step = 0
        self._ow = w  # overlay (= poker window) width
        self._oh = h

        # Drawing state
        self._drawing = False
        self._pt1: Optional[QPoint] = None
        self._pt2: Optional[QPoint] = None
        self._confirmed: Optional[QRect] = None  # drawn, awaiting Enter

        # Instruction panel (draggable, top-center)
        panel_w = min(680, w - 20)
        self._panel_rect = QRect((w - panel_w) // 2, 10, panel_w, 74)
        self._panel_dragging = False
        self._panel_drag_offset: Optional[QPoint] = None

        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setMouseTracking(True)
        self.setGeometry(x, y, w, h)

    # ------------------------------------------------------------------ paint

    def paintEvent(self, _event) -> None:
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Faint overlay tint so the active calibration state is obvious
        p.fillRect(self.rect(), QColor(0, 0, 0, 45))

        # Already-confirmed regions (blue outlines)
        p.setPen(QPen(QColor(100, 120, 255), 1))
        label_font = QFont("Consolas", 8)
        p.setFont(label_font)
        for r in self._regions:
            px, py, pw, ph = r.to_pixels(self._ow, self._oh)
            p.setPen(QPen(QColor(100, 120, 255), 1))
            p.drawRect(px, py, pw, ph)
            p.setPen(QPen(QColor(180, 190, 255), 1))
            p.drawText(px + 3, py + 12, r.key)

        # In-progress drag (yellow)
        if self._drawing and self._pt1 and self._pt2:
            rect = QRect(self._pt1, self._pt2).normalized()
            p.setPen(QPen(QColor(255, 240, 0), 2))
            p.setBrush(QBrush(QColor(255, 240, 0, 28)))
            p.drawRect(rect)

        # Confirmed, awaiting Enter (green)
        if self._confirmed:
            p.setPen(QPen(QColor(0, 230, 80), 2))
            p.setBrush(QBrush(QColor(0, 230, 80, 28)))
            p.drawRect(self._confirmed)

        # Instruction panel background
        pr = self._panel_rect
        p.setPen(Qt.PenStyle.NoPen)
        p.setBrush(QBrush(QColor(12, 14, 18, 215)))
        p.drawRoundedRect(pr, 8, 8)

        key_name, display_name, _, optional = self._sequence[self._step]
        total = len(self._sequence)

        # Line 1 — current region
        f1 = QFont("Consolas", 11)
        f1.setBold(True)
        p.setFont(f1)
        p.setPen(QPen(QColor(255, 255, 255)))
        p.drawText(pr.x() + 12, pr.y() + 28,
                   f"[{self._step + 1}/{total}]  Draw box around:  {display_name}")

        # Line 2 — controls
        skip_hint = "  S=skip" if optional else ""
        f2 = QFont("Consolas", 8)
        p.setFont(f2)
        p.setPen(QPen(QColor(130, 170, 255)))
        p.drawText(pr.x() + 12, pr.y() + 54,
                   f"Enter=confirm{skip_hint}   Backspace=undo   R=clear-box   Esc=abort"
                   "   (drag this panel to move it)")

        p.end()

    # ------------------------------------------------------------------ mouse

    def mousePressEvent(self, event) -> None:
        if event.button() != Qt.MouseButton.LeftButton:
            return
        pos = event.pos()
        if self._panel_rect.contains(pos):
            self._panel_dragging = True
            self._panel_drag_offset = pos - self._panel_rect.topLeft()
        else:
            self._drawing = True
            self._pt1 = pos
            self._pt2 = pos
            self._confirmed = None
            self.update()

    def mouseMoveEvent(self, event) -> None:
        pos = event.pos()
        if self._panel_dragging and self._panel_drag_offset is not None:
            self._panel_rect.moveTopLeft(pos - self._panel_drag_offset)
            self.update()
        elif self._drawing:
            self._pt2 = pos
            self.update()

    def mouseReleaseEvent(self, event) -> None:
        if event.button() != Qt.MouseButton.LeftButton:
            return
        if self._panel_dragging:
            self._panel_dragging = False
            self._panel_drag_offset = None
        elif self._drawing:
            self._drawing = False
            self._pt2 = event.pos()
            rect = QRect(self._pt1, self._pt2).normalized()
            if rect.width() > 2 and rect.height() > 2:
                self._confirmed = rect
            self.update()

    # ---------------------------------------------------------------- keyboard

    def keyPressEvent(self, event) -> None:
        key = event.key()
        key_name, _, seat, optional = self._sequence[self._step]

        if key in (Qt.Key.Key_Return, Qt.Key.Key_Enter, Qt.Key.Key_Space):
            if self._confirmed:
                r = self._confirmed
                self._regions.append(RegionDef(
                    key=key_name,
                    x_pct=_pct(r.x(), self._ow),
                    y_pct=_pct(r.y(), self._oh),
                    w_pct=_pct(r.width(), self._ow),
                    h_pct=_pct(r.height(), self._oh),
                    seat=seat,
                ))
                self._confirmed = None
                self._advance()

        elif key == Qt.Key.Key_S and optional:
            self._confirmed = None
            self._advance()

        elif key == Qt.Key.Key_Backspace:
            if self._regions:
                self._regions.pop()
                self._step = max(0, self._step - 1)
            self._confirmed = None
            self.update()

        elif key == Qt.Key.Key_R:
            self._confirmed = None
            self._drawing = False
            self.update()

        elif key == Qt.Key.Key_Escape:
            self.done.emit(None)
            QApplication.quit()

    # --------------------------------------------------------------- internal

    def _advance(self) -> None:
        self._step += 1
        if self._step >= len(self._sequence):
            self.done.emit(self._regions)
            QApplication.quit()
        else:
            self.update()


# ---------------------------------------------------------------------------


def run_calibration(
    window_title: str,
    profile_name: str,
    output_dir: str,
    include_seats: bool = False,
) -> Optional[TableProfile]:
    """
    Launch the calibration overlay on top of the poker window.

    Returns a saved TableProfile on success, None if aborted.
    """
    print(f"Looking for window: '{window_title}'...")
    info = find_window(window_title)
    if info:
        bx, by, bw, bh = info["bbox"]
        win_w, win_h = bw, bh
        print(f"Found: '{info['title']}' ({win_w}x{win_h}) at ({bx},{by})")
    else:
        print("Window not found — calibrating over the primary screen.")
        app_ref = QApplication.instance() or QApplication(sys.argv)
        screen = app_ref.primaryScreen().geometry()
        bx, by, win_w, win_h = screen.x(), screen.y(), screen.width(), screen.height()

    sequence: list[tuple[str, str, Optional[str], bool]] = list(_REGION_SEQUENCE)
    if include_seats:
        sequence += _SEAT_SEQUENCE

    print(f"Starting calibration: {len(sequence)} regions to define.")
    print("Drag a rectangle around each region when prompted.")
    print("Controls: Enter=confirm  S=skip(optional)  Backspace=undo  R=clear  Esc=abort\n")

    app = QApplication.instance() or QApplication(sys.argv)

    result_holder: list[Optional[list[RegionDef]]] = [None]

    overlay = CalibratorOverlay(bx, by, win_w, win_h, sequence)
    overlay.done.connect(lambda regions: result_holder.__setitem__(0, regions))
    overlay.show()
    overlay.raise_()
    overlay.activateWindow()

    app.exec()

    regions = result_holder[0]
    if regions is None:
        print("Calibration aborted.")
        return None

    hero = [r for r in regions if r.key.startswith("hero_")]
    community = [r for r in regions if r.key in ("flop_1", "flop_2", "flop_3", "turn", "river")]
    seats = [r for r in regions if r.key.startswith("seat_")]
    pot = next((r for r in regions if r.key == "pot_region"), None)
    to_call = next((r for r in regions if r.key == "to_call_region"), None)

    profile = TableProfile(
        name=profile_name,
        window_title=window_title,
        window_width=win_w,
        window_height=win_h,
        hero_cards=hero,
        community_cards=community,
        seat_cards=seats,
        pot_region=pot,
        to_call_region=to_call,
    )

    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, f"{profile_name}.json")
    save_profile(profile, path)
    print(f"\nProfile saved: {path}")
    print(f"  Hero cards:      {len(hero)}")
    print(f"  Community cards: {len(community)}")
    print(f"  Seat cards:      {len(seats)}")
    return profile
