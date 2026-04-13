"""
Data augmentation pipeline.

Reads images from data/raw/{label}/ and writes augmented copies to
data/augmented/{label}/ at 64x64 RGB.

Augmentations applied per source image (configurable):
  - Random brightness/contrast
  - Random rotation (+/- 8 degrees)
  - Gaussian blur (occasionally)
  - Affine warp (slight perspective distortion)
  - HSV jitter (hue, saturation, value)
  - Random crop + resize (within 10%)
  - Horizontal flip (disabled by default — card suits are asymmetric)

Target: ~500 augmented images per class.

Usage:
    python scripts/augment.py
    python scripts/augment.py --target 1000 --raw-dir data/raw --out-dir data/augmented
"""

import argparse
import os
import random
import sys

import cv2
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.common.constants import CARD_LABELS

CARD_SIZE = (64, 64)
DEFAULT_TARGET = 500


def _random_brightness_contrast(img: np.ndarray) -> np.ndarray:
    alpha = random.uniform(0.7, 1.3)   # contrast
    beta = random.randint(-30, 30)      # brightness
    return np.clip(img.astype(np.float32) * alpha + beta, 0, 255).astype(np.uint8)


def _random_rotation(img: np.ndarray) -> np.ndarray:
    angle = random.uniform(-8, 8)
    h, w = img.shape[:2]
    M = cv2.getRotationMatrix2D((w / 2, h / 2), angle, 1.0)
    return cv2.warpAffine(img, M, (w, h), flags=cv2.INTER_LINEAR,
                          borderMode=cv2.BORDER_REFLECT_101)


def _random_blur(img: np.ndarray) -> np.ndarray:
    if random.random() < 0.3:
        k = random.choice([3, 5])
        return cv2.GaussianBlur(img, (k, k), 0)
    return img


def _random_affine(img: np.ndarray) -> np.ndarray:
    h, w = img.shape[:2]
    max_shift = int(w * 0.06)
    pts1 = np.float32([[0, 0], [w, 0], [0, h]])
    pts2 = pts1 + np.random.randint(-max_shift, max_shift + 1, pts1.shape).astype(np.float32)
    M = cv2.getAffineTransform(pts1, pts2)
    return cv2.warpAffine(img, M, (w, h), flags=cv2.INTER_LINEAR,
                          borderMode=cv2.BORDER_REFLECT_101)


def _random_hsv_jitter(img: np.ndarray) -> np.ndarray:
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV).astype(np.int32)
    hsv[:, :, 0] = np.clip(hsv[:, :, 0] + random.randint(-10, 10), 0, 179)
    hsv[:, :, 1] = np.clip(hsv[:, :, 1] + random.randint(-30, 30), 0, 255)
    hsv[:, :, 2] = np.clip(hsv[:, :, 2] + random.randint(-20, 20), 0, 255)
    return cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR)


def _random_crop_resize(img: np.ndarray) -> np.ndarray:
    h, w = img.shape[:2]
    margin = int(min(h, w) * 0.1)
    if margin < 1:
        return img
    x1 = random.randint(0, margin)
    y1 = random.randint(0, margin)
    x2 = w - random.randint(0, margin)
    y2 = h - random.randint(0, margin)
    cropped = img[y1:y2, x1:x2]
    return cv2.resize(cropped, (w, h), interpolation=cv2.INTER_AREA)


def augment_image(img: np.ndarray) -> np.ndarray:
    """Apply a random combination of augmentations to one image."""
    img = _random_brightness_contrast(img)
    img = _random_rotation(img)
    img = _random_affine(img)
    img = _random_hsv_jitter(img)
    img = _random_blur(img)
    img = _random_crop_resize(img)
    return img


def augment_class(label: str, raw_dir: str, out_dir: str, target: int) -> int:
    """
    Augment all source images for one label to reach `target` total images.
    Returns the number of images written.
    """
    src_dir = os.path.join(raw_dir, label)
    dst_dir = os.path.join(out_dir, label)
    os.makedirs(dst_dir, exist_ok=True)

    sources = [
        f for f in os.listdir(src_dir) if f.lower().endswith((".png", ".jpg", ".jpeg"))
    ] if os.path.isdir(src_dir) else []

    if not sources:
        print(f"  [{label}] No source images found in {src_dir} — skipping.")
        return 0

    written = 0
    idx = 0
    while written < target:
        src_file = sources[idx % len(sources)]
        src_path = os.path.join(src_dir, src_file)
        img = cv2.imread(src_path)
        if img is None:
            idx += 1
            continue

        img = cv2.resize(img, CARD_SIZE, interpolation=cv2.INTER_AREA)
        aug = augment_image(img)
        out_path = os.path.join(dst_dir, f"aug_{written:05d}.png")
        cv2.imwrite(out_path, aug)
        written += 1
        idx += 1

    return written


def main() -> None:
    parser = argparse.ArgumentParser(description="Augment card images for training")
    parser.add_argument("--raw-dir", default="data/raw", help="Input directory")
    parser.add_argument("--out-dir", default="data/augmented", help="Output directory")
    parser.add_argument("--target", type=int, default=DEFAULT_TARGET,
                        help="Target number of augmented images per class")
    parser.add_argument("--labels", nargs="*", default=None,
                        help="Only augment these labels (default: all 54)")
    args = parser.parse_args()

    base = os.path.join(os.path.dirname(__file__), "..")
    raw_dir = os.path.join(base, args.raw_dir)
    out_dir = os.path.join(base, args.out_dir)

    labels = args.labels if args.labels else CARD_LABELS
    total = 0

    print(f"Augmenting {len(labels)} classes -> {args.target} images each")
    print(f"  raw:  {raw_dir}")
    print(f"  out:  {out_dir}\n")

    for label in labels:
        n = augment_class(label, raw_dir, out_dir, args.target)
        total += n
        if n:
            print(f"  [{label}] {n} images written")

    print(f"\nDone. {total} total images across {len(labels)} classes.")


if __name__ == "__main__":
    main()
