"""
Interactive card image collector.

Opens a live view of a screen region and lets the user save card crops
to data/raw/{label}/ using keyboard shortcuts.

Usage:
    python -m src.capture.collector --region 100 200 300 400
    python -m src.capture.collector  # prompts for region interactively

Controls:
    Type rank+suit (e.g. 'ah' for Ace of Hearts) then press Enter to save.
    Type 'empty' + Enter to save an empty slot image.
    Type 'back' + Enter to save a card-back image.
    Press Escape or 'q' to quit.
"""

import argparse
import os
import sys
import time

import cv2
import numpy as np

# Allow running as script from railbird/
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from src.capture.screenshot import grab_region, set_dpi_aware
from src.common.constants import CARD_LABELS, LABEL_TO_IDX

DATA_RAW_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data", "raw")
CARD_SIZE = (64, 64)


def _next_filename(label_dir: str) -> str:
    """Return next available filename like img_00042.png."""
    existing = [f for f in os.listdir(label_dir) if f.endswith(".png")]
    return f"img_{len(existing):05d}.png"


def _save_image(frame: np.ndarray, label: str) -> str:
    """Resize frame to 64x64 RGB and save to data/raw/{label}/. Returns saved path."""
    label_dir = os.path.join(DATA_RAW_DIR, label)
    os.makedirs(label_dir, exist_ok=True)
    resized = cv2.resize(frame, CARD_SIZE, interpolation=cv2.INTER_AREA)
    path = os.path.join(label_dir, _next_filename(label_dir))
    cv2.imwrite(path, resized)
    return path


def run_collector(bbox: tuple[int, int, int, int]) -> None:
    """
    Run the interactive collector.

    Args:
        bbox: (left, top, width, height) of the region to watch.
    """
    print("\n=== Card Collector ===")
    print("Live view of your selected region.")
    print("Type a card label (e.g. 'Ah', '2c', 'Td') then press Enter to save.")
    print("Special labels: 'empty', 'back'")
    print("Press Escape or type 'q' + Enter to quit.\n")

    window_name = "Card Collector — type label + Enter to save"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(window_name, 400, 400)

    input_buffer = ""
    status_msg = "Ready"
    status_color = (180, 180, 180)
    status_until = 0.0

    while True:
        frame = grab_region(bbox)
        display = cv2.resize(frame, (400, 400), interpolation=cv2.INTER_NEAREST)

        # Draw input buffer overlay
        now = time.time()
        msg = f"Label: {input_buffer}_" if input_buffer else "Type label..."
        cv2.rectangle(display, (0, 360), (400, 400), (30, 30, 30), -1)
        cv2.putText(display, msg, (8, 388), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)

        if now < status_until:
            cv2.rectangle(display, (0, 320), (400, 360), (30, 30, 30), -1)
            cv2.putText(display, status_msg, (8, 348), cv2.FONT_HERSHEY_SIMPLEX, 0.55, status_color, 1)

        cv2.imshow(window_name, display)

        key = cv2.waitKey(30) & 0xFF

        if key == 27:  # Escape
            break
        elif key == 13 or key == 10:  # Enter
            label = input_buffer.strip().lower()
            input_buffer = ""

            if label == "q":
                break

            # Normalize label: 'ah' -> 'Ah', '2c' -> '2c', 'empty' -> 'empty'
            if len(label) == 2 and label[0].isalpha():
                label = label[0].upper() + label[1].lower()
            elif len(label) == 3 and label[:2].isdigit():  # e.g. '10h' — treat as Th
                label = "T" + label[-1].lower()

            if label not in LABEL_TO_IDX:
                status_msg = f"Unknown label: '{label}' — try again"
                status_color = (0, 0, 220)
                status_until = now + 2.0
                continue

            path = _save_image(frame, label)
            count = len(os.listdir(os.path.join(DATA_RAW_DIR, label)))
            status_msg = f"Saved {label} ({count} total) -> {os.path.basename(path)}"
            status_color = (0, 200, 0)
            status_until = now + 2.0
            print(status_msg)

        elif key == 8:  # Backspace
            input_buffer = input_buffer[:-1]
        elif 32 <= key < 127:  # Printable ASCII
            input_buffer += chr(key)

    cv2.destroyAllWindows()


def _select_region_interactively() -> tuple[int, int, int, int]:
    """Capture a fullscreen screenshot and let the user drag a crop region."""
    from src.capture.screenshot import grab_fullscreen
    print("Capturing fullscreen. Drag a rectangle over the card region you want to watch.")
    screen = grab_fullscreen(monitor_index=1)
    roi = cv2.selectROI("Select Card Region (drag, then press Enter/Space)", screen, fromCenter=False)
    cv2.destroyAllWindows()
    x, y, w, h = roi
    if w == 0 or h == 0:
        print("No region selected. Exiting.")
        sys.exit(1)
    return (x, y, w, h)


def main() -> None:
    set_dpi_aware()
    parser = argparse.ArgumentParser(description="Interactive card image collector")
    parser.add_argument(
        "--region", type=int, nargs=4, metavar=("LEFT", "TOP", "WIDTH", "HEIGHT"),
        help="Screen region to watch. If omitted, prompts interactively."
    )
    args = parser.parse_args()

    if args.region:
        bbox = tuple(args.region)
    else:
        bbox = _select_region_interactively()

    run_collector(bbox)


if __name__ == "__main__":
    main()
