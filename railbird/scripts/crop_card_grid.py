"""
Crop a playing-card grid image into individual labeled training images.

Takes a single image showing all cards arranged in a grid (e.g. a 13x4 deck
sheet), slices it into one cell per card, resizes each to 64x64, and saves
them to data/raw/{label}/ so augment.py can use them.

The two special classes (empty, back) are not present in standard card grids
and must be collected separately via collector.py or generate_synthetic_cards.py.

Usage:
    python scripts/crop_card_grid.py --image path/to/deck.png
    python scripts/crop_card_grid.py --image deck.png --rows shdc --cols A23456789TJQK
    python scripts/crop_card_grid.py --image deck.png --padding 0.08 --size 64
"""

import argparse
import os
import sys

import cv2
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from src.common.constants import RANKS, SUITS

DEFAULT_ROWS = "cdhs"
DEFAULT_COLS = "A23456789TJQK"
OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "raw")


def _next_index(folder: str) -> int:
    existing = [f for f in os.listdir(folder) if f.endswith(".png")]
    return len(existing) + 1


def crop_grid(image_path: str, rows: str, cols: str, out_dir: str, size: int, padding: float) -> None:
    img = cv2.imread(image_path)
    if img is None:
        sys.exit(f"Error: could not load image: {image_path}")

    h, w = img.shape[:2]
    n_rows, n_cols = len(rows), len(cols)
    cell_w = w / n_cols
    cell_h = h / n_rows

    saved = 0
    for r_idx, suit in enumerate(rows):
        for c_idx, rank in enumerate(cols):
            label = f"{rank}{suit}"

            x0 = int(c_idx * cell_w)
            y0 = int(r_idx * cell_h)
            x1 = int((c_idx + 1) * cell_w)
            y1 = int((r_idx + 1) * cell_h)

            if padding > 0:
                px = int((x1 - x0) * padding)
                py = int((y1 - y0) * padding)
                x0, y0 = x0 + px, y0 + py
                x1, y1 = x1 - px, y1 - py

            cell = img[y0:y1, x0:x1]
            cell = cv2.resize(cell, (size, size), interpolation=cv2.INTER_AREA)

            label_dir = os.path.join(out_dir, label)
            os.makedirs(label_dir, exist_ok=True)
            idx = _next_index(label_dir)
            out_path = os.path.join(label_dir, f"grid_{idx:03d}.png")
            cv2.imwrite(out_path, cell)
            saved += 1
            print(f"  [{label}] -> {out_path}")

    print(f"\nDone. {saved} images saved to {out_dir}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Crop a card grid image into per-label training images.")
    parser.add_argument("--image", required=True, help="Path to the card grid image.")
    parser.add_argument("--rows", default=DEFAULT_ROWS,
                        help=f"Suit order top-to-bottom, one char each from cdhs. Default: {DEFAULT_ROWS}")
    parser.add_argument("--cols", default=DEFAULT_COLS,
                        help=f"Rank order left-to-right, chars from 23456789TJQKA. Default: {DEFAULT_COLS}")
    parser.add_argument("--out-dir", default=OUT_DIR, help="Root output directory (default: data/raw).")
    parser.add_argument("--size", type=int, default=64, help="Output image size in pixels (default: 64).")
    parser.add_argument("--padding", type=float, default=0.05,
                        help="Fractional inner border to trim from each cell (default: 0.05).")
    args = parser.parse_args()

    invalid_suits = [c for c in args.rows if c not in SUITS]
    if invalid_suits:
        sys.exit(f"Error: unknown suit chars in --rows: {invalid_suits}. Valid: {SUITS}")
    invalid_ranks = [c for c in args.cols if c not in RANKS]
    if invalid_ranks:
        sys.exit(f"Error: unknown rank chars in --cols: {invalid_ranks}. Valid: {RANKS}")

    crop_grid(
        image_path=args.image,
        rows=args.rows,
        cols=args.cols,
        out_dir=args.out_dir,
        size=args.size,
        padding=args.padding,
    )


if __name__ == "__main__":
    main()
