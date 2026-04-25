"""
Table calibration tool.

Presents a screenshot of the poker window and guides the user through
dragging rectangles for each card region. Saves the result as a TableProfile.

Controls during rectangle drawing:
    Drag left mouse button — draw region
    Enter / Space          — confirm current region and advance
    Backspace              — redo previous region
    Escape                 — abort calibration

Usage (via scripts/calibrate.py):
    python scripts/calibrate.py --window "PokerStars" --profile-name "ps_6max"
"""

import os
import sys
from typing import Optional

import cv2
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from src.capture.cropper import RegionDef, TableProfile, save_profile
from src.capture.screenshot import grab_fullscreen
from src.capture.window import capture_window, find_window


# Ordered list of regions to calibrate.
# Format: (key, display_name, seat_name_or_None, optional)
_REGION_SEQUENCE = [
    ("hero_1",       "Hero Card 1",                     None, False),
    ("hero_2",       "Hero Card 2",                     None, False),
    ("flop_1",       "Community: Flop 1",               None, False),
    ("flop_2",       "Community: Flop 2",               None, False),
    ("flop_3",       "Community: Flop 3",               None, False),
    ("turn",         "Community: Turn",                 None, False),
    ("river",        "Community: River",                None, False),
    ("pot_region",   "Pot total (S=skip if no OCR)",    None, True),
    ("to_call_region", "To-call amount (S=skip if no OCR)", None, True),
]

# Optional seat opponent card regions (2 cards each, up to 5 opponents for 6-max)
_SEAT_SEQUENCE = [
    (f"seat_{s}_card_{c}", f"Seat {s} Card {c}", f"seat_{s}", False)
    for s in range(1, 6)
    for c in range(1, 3)
]


def _pct(val: int, total: int) -> float:
    return val / total if total > 0 else 0.0


class Calibrator:
    """Interactive region selection tool using an OpenCV window."""

    def __init__(self, frame: np.ndarray, win_w: int, win_h: int) -> None:
        self._frame = frame.copy()
        self._win_w = win_w
        self._win_h = win_h
        self._regions: list[RegionDef] = []

        self._drawing = False
        self._pt1: Optional[tuple[int, int]] = None
        self._pt2: Optional[tuple[int, int]] = None
        self._confirmed: Optional[tuple[int, int, int, int]] = None  # x,y,w,h in display coords

        # Display scaling (the frame may differ from actual window size)
        self._display_w = frame.shape[1]
        self._display_h = frame.shape[0]

    def _mouse_callback(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self._drawing = True
            self._pt1 = (x, y)
            self._pt2 = (x, y)
            self._confirmed = None
        elif event == cv2.EVENT_MOUSEMOVE and self._drawing:
            self._pt2 = (x, y)
        elif event == cv2.EVENT_LBUTTONUP:
            self._drawing = False
            self._pt2 = (x, y)
            x1, y1 = self._pt1
            x2, y2 = self._pt2
            rx, ry = min(x1, x2), min(y1, y2)
            rw, rh = abs(x2 - x1), abs(y2 - y1)
            if rw > 2 and rh > 2:
                self._confirmed = (rx, ry, rw, rh)

    def _draw_overlay(self, canvas: np.ndarray, label: str, step: int, total: int) -> np.ndarray:
        out = canvas.copy()
        # In-progress rectangle
        if self._drawing and self._pt1 and self._pt2:
            cv2.rectangle(out, self._pt1, self._pt2, (0, 255, 255), 2)
        # Confirmed rectangle
        if self._confirmed:
            x, y, w, h = self._confirmed
            cv2.rectangle(out, (x, y), (x + w, y + h), (0, 255, 0), 2)
        # Already-defined regions
        for r in self._regions:
            px, py, pw, ph = r.to_pixels(self._display_w, self._display_h)
            cv2.rectangle(out, (px, py), (px + pw, py + ph), (100, 100, 255), 1)
            cv2.putText(out, r.key, (px + 2, py + 12),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.35, (200, 200, 255), 1)
        # Instruction bar
        bar_h = 50
        cv2.rectangle(out, (0, 0), (out.shape[1], bar_h), (20, 20, 20), -1)
        cv2.putText(out, f"[{step+1}/{total}] Draw: {label}",
                    (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 1)
        cv2.putText(out, "Enter=confirm  S=skip  Backspace=redo  Escape=abort",
                    (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.42, (160, 160, 160), 1)
        return out

    def run(self, sequence: list[tuple[str, str, Optional[str]]]) -> Optional[list[RegionDef]]:
        """
        Run the calibration UI for the given sequence.

        Returns list of RegionDef on success, None if aborted.
        """
        wname = "Calibration — follow the instructions above"
        cv2.namedWindow(wname, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(wname, min(self._display_w, 1280), min(self._display_h + 50, 960))
        cv2.setMouseCallback(wname, self._mouse_callback)

        step = 0
        skipped: set[str] = set()

        while step < len(sequence):
            key_name, display_name, seat = sequence[step]
            optional = sequence[step][3] if len(sequence[step]) > 3 else False
            canvas = self._draw_overlay(self._frame, display_name, step, len(sequence))
            cv2.imshow(wname, canvas)
            k = cv2.waitKey(30) & 0xFF

            if k == 27:  # Escape — abort
                cv2.destroyWindow(wname)
                return None

            elif k in (ord('s'), ord('S')) and optional:  # S — skip optional region
                skipped.add(key_name)
                step += 1

            elif k in (13, 32):  # Enter or Space — confirm
                if self._confirmed:
                    rx, ry, rw, rh = self._confirmed
                    # Convert display coords to percentage of actual window size
                    x_pct = _pct(rx, self._display_w)
                    y_pct = _pct(ry, self._display_h)
                    w_pct = _pct(rw, self._display_w)
                    h_pct = _pct(rh, self._display_h)
                    region = RegionDef(
                        key=key_name,
                        x_pct=x_pct, y_pct=y_pct,
                        w_pct=w_pct, h_pct=h_pct,
                        seat=seat,
                    )
                    self._regions.append(region)
                    self._confirmed = None
                    step += 1

            elif k == 8:  # Backspace — redo last
                if self._regions:
                    self._regions.pop()
                    step = max(0, step - 1)
                self._confirmed = None

        cv2.destroyWindow(wname)
        return self._regions


def run_calibration(
    window_title: str,
    profile_name: str,
    output_dir: str,
    include_seats: bool = False,
) -> Optional[TableProfile]:
    """
    Capture the poker window and run the calibration UI.

    Returns a saved TableProfile on success, None if aborted.
    """
    print(f"Looking for window: '{window_title}'...")
    info = find_window(window_title)
    if info:
        frame = capture_window(info["hwnd"])
        win_w, win_h = info["bbox"][2], info["bbox"][3]
        print(f"Found: '{info['title']}' ({win_w}x{win_h})")
    else:
        print("Window not found. Using full screen instead.")
        frame = grab_fullscreen(monitor_index=1)
        win_w, win_h = frame.shape[1], frame.shape[0]

    if frame is None:
        print("Failed to capture screen.")
        return None

    sequence = list(_REGION_SEQUENCE)
    if include_seats:
        sequence += _SEAT_SEQUENCE

    print(f"Starting calibration: {len(sequence)} regions to define.")
    print("Drag a rectangle around each region when prompted.\n")

    calibrator = Calibrator(frame, win_w, win_h)
    regions = calibrator.run(sequence)

    if regions is None:
        print("Calibration aborted.")
        return None

    # Split regions into typed buckets
    hero = [r for r in regions if r.key.startswith("hero_")]
    community = [r for r in regions if r.key in
                 ("flop_1", "flop_2", "flop_3", "turn", "river")]
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
