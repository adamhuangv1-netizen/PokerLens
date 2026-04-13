"""
Generate synthetic raw card images for all 54 classes.

Creates programmatically-rendered playing card images and saves them to
data/raw/{label}/ so that scripts/augment.py has source material to work with.

Each class gets `--count` source images (default 20) with slight rendering
variations so augmentation sees non-identical copies.

Usage:
    python scripts/generate_synthetic_cards.py
    python scripts/generate_synthetic_cards.py --count 30 --size 128
"""

import argparse
import os
import random
import sys

from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from src.common.constants import CARD_LABELS, RANKS, SUITS

SUIT_SYMBOLS = {"c": "♣", "d": "♦", "h": "♥", "s": "♠"}
SUIT_COLORS  = {"c": (20, 20, 20), "d": (200, 20, 20), "h": (200, 20, 20), "s": (20, 20, 20)}
RANK_DISPLAY = {"T": "10", "J": "J", "Q": "Q", "K": "K", "A": "A"}

# Suit pip positions (relative to card size, for simple center pips)
_PIP_GRIDS = {
    1: [(0.5, 0.5)],
    2: [(0.5, 0.28), (0.5, 0.72)],
    3: [(0.5, 0.20), (0.5, 0.50), (0.5, 0.80)],
    4: [(0.30, 0.28), (0.70, 0.28), (0.30, 0.72), (0.70, 0.72)],
    5: [(0.30, 0.28), (0.70, 0.28), (0.50, 0.50), (0.30, 0.72), (0.70, 0.72)],
    6: [(0.30, 0.22), (0.70, 0.22), (0.30, 0.50), (0.70, 0.50), (0.30, 0.78), (0.70, 0.78)],
    7: [(0.30, 0.22), (0.70, 0.22), (0.50, 0.35), (0.30, 0.50), (0.70, 0.50), (0.30, 0.78), (0.70, 0.78)],
    8: [(0.30, 0.22), (0.70, 0.22), (0.50, 0.33), (0.30, 0.50), (0.70, 0.50), (0.50, 0.67), (0.30, 0.78), (0.70, 0.78)],
    9: [(0.30, 0.20), (0.70, 0.20), (0.30, 0.38), (0.70, 0.38), (0.50, 0.50), (0.30, 0.62), (0.70, 0.62), (0.30, 0.80), (0.70, 0.80)],
    10: [(0.30, 0.20), (0.70, 0.20), (0.50, 0.30), (0.30, 0.40), (0.70, 0.40), (0.30, 0.60), (0.70, 0.60), (0.50, 0.70), (0.30, 0.80), (0.70, 0.80)],
}


def _rank_to_pips(rank: str) -> int:
    mapping = {"2": 2, "3": 3, "4": 4, "5": 5, "6": 6,
               "7": 7, "8": 8, "9": 9, "T": 10,
               "J": 1, "Q": 1, "K": 1, "A": 1}
    return mapping[rank]


def _try_load_font(size: int):
    """Try to load a reasonable font; fall back to PIL default."""
    candidates = [
        "arial.ttf", "Arial.ttf",
        "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/calibri.ttf",
        "C:/Windows/Fonts/times.ttf",
        "C:/Windows/Fonts/verdana.ttf",
    ]
    for path in candidates:
        try:
            return ImageFont.truetype(path, size)
        except (IOError, OSError):
            continue
    return ImageFont.load_default()


def render_card(label: str, size: int = 64, variation: int = 0) -> Image.Image:
    """Render a single card image with slight per-variation noise."""
    rng = random.Random(hash((label, variation)))

    w, h = size, size

    # Card background: white with tiny random tint
    r_tint = rng.randint(245, 255)
    g_tint = rng.randint(245, 255)
    b_tint = rng.randint(245, 255)
    img = Image.new("RGB", (w, h), (r_tint, g_tint, b_tint))
    draw = ImageDraw.Draw(img)

    # Card border
    border_w = max(1, size // 32)
    border_color = (rng.randint(160, 200), rng.randint(160, 200), rng.randint(160, 200))
    draw.rectangle([0, 0, w - 1, h - 1], outline=border_color, width=border_w)

    if label == "empty":
        # Mostly blank with faint table-felt green tint
        img = Image.new("RGB", (w, h), (
            rng.randint(30, 60),
            rng.randint(80, 120),
            rng.randint(30, 60),
        ))
        # Add a little noise to help the model learn the class
        import numpy as np
        arr = np.array(img, dtype=np.int32)
        noise = np.random.RandomState(variation).randint(-15, 15, arr.shape)
        arr = np.clip(arr + noise, 0, 255).astype(np.uint8)
        return Image.fromarray(arr)

    if label == "back":
        # Blue card-back with crosshatch pattern
        img = Image.new("RGB", (w, h), (30, 60, 160))
        draw = ImageDraw.Draw(img)
        # Border
        draw.rectangle([2, 2, w - 3, h - 3], outline=(200, 210, 240), width=1)
        # Diagonal lines
        step = max(4, size // 12)
        line_color = (20, 45, 140)
        for i in range(-h, w + h, step):
            draw.line([(i, 0), (i + h, h)], fill=line_color, width=1)
            draw.line([(i + h, 0), (i, h)], fill=line_color, width=1)
        return img

    # Normal card
    rank, suit = label[:-1], label[-1]
    color = SUIT_COLORS[suit]
    sym = SUIT_SYMBOLS[suit]
    display_rank = RANK_DISPLAY.get(rank, rank)

    font_corner = _try_load_font(max(8, size // 6))
    font_center = _try_load_font(max(12, size // 4))

    # Top-left rank + suit
    margin = max(2, size // 20)
    draw.text((margin, margin), display_rank, font=font_corner, fill=color)
    draw.text((margin, margin + size // 5), sym, font=font_corner, fill=color)

    # Bottom-right (rotated 180°) rank + suit
    # Draw to a small sub-image and rotate
    sub_w, sub_h = size // 3, size // 3
    sub = Image.new("RGB", (sub_w, sub_h), (r_tint, g_tint, b_tint))
    sub_draw = ImageDraw.Draw(sub)
    sub_draw.text((0, 0), display_rank, font=font_corner, fill=color)
    sub_draw.text((0, sub_h // 2), sym, font=font_corner, fill=color)
    sub_rot = sub.rotate(180)
    img.paste(sub_rot, (w - sub_w - margin, h - sub_h - margin))

    # Center pip(s) or face-card letter
    pip_count = _rank_to_pips(rank)
    if rank in ("J", "Q", "K"):
        # Face card: big letter in center
        bbox = draw.textbbox((0, 0), display_rank, font=font_center)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
        cx = (w - tw) // 2
        cy = (h - th) // 2
        draw.text((cx, cy), display_rank, font=font_center, fill=color)
    else:
        # Pips
        pip_size = max(3, size // 14)
        for (px, py) in _PIP_GRIDS.get(pip_count, _PIP_GRIDS[1]):
            cx = int(px * w)
            cy = int(py * h)
            draw.text((cx - pip_size, cy - pip_size), sym, font=font_corner, fill=color)

    return img


def generate_all(out_dir: str, count: int, size: int) -> None:
    os.makedirs(out_dir, exist_ok=True)
    total = 0
    print(f"Generating {count} images per class ({len(CARD_LABELS)} classes) at {size}x{size}px")
    for label in CARD_LABELS:
        label_dir = os.path.join(out_dir, label)
        os.makedirs(label_dir, exist_ok=True)
        for i in range(count):
            img = render_card(label, size=size, variation=i)
            img.save(os.path.join(label_dir, f"{label}_{i:03d}.png"))
        total += count
        print(f"  [{label}] {count} images")
    print(f"\nDone. {total} total source images in {out_dir}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate synthetic raw card images")
    parser.add_argument("--out-dir", default="data/raw",
                        help="Output directory (default: data/raw)")
    parser.add_argument("--count", type=int, default=20,
                        help="Images per class (default: 20)")
    parser.add_argument("--size", type=int, default=64,
                        help="Image size in pixels (default: 64)")
    args = parser.parse_args()

    base = os.path.join(os.path.dirname(__file__), "..")
    out_dir = os.path.join(base, args.out_dir)
    generate_all(out_dir, args.count, args.size)


if __name__ == "__main__":
    main()
