"""
ChipOcr — reads chip amounts from a cropped screen region.

Designed for poker pot/bet displays that show values like "$1,234" or "1234".
Uses Tesseract OCR via pytesseract (system Tesseract required).

Install:
    pip install pytesseract
    # Windows: download installer from https://github.com/UB-Mannheim/tesseract/wiki
    # Add install dir (e.g. C:/Program Files/Tesseract-OCR) to PATH

Usage:
    ocr = ChipOcr()
    amount = ocr.read(bgr_image)  # returns float or None
"""

from typing import Optional

import cv2
import numpy as np

try:
    import pytesseract
    # UB Mannheim installer puts tesseract in AppData/Local on Windows
    import os, shutil
    if not shutil.which("tesseract"):
        _fallback = os.path.expandvars(
            r"%LOCALAPPDATA%\Programs\Tesseract-OCR\tesseract.exe"
        )
        if os.path.isfile(_fallback):
            pytesseract.pytesseract.tesseract_cmd = _fallback
    _PYTESSERACT_AVAILABLE = True
except ImportError:
    _PYTESSERACT_AVAILABLE = False

_TESSERACT_CONFIG = "--psm 7 -c tessedit_char_whitelist=0123456789.,$"


class ChipOcr:
    """
    Reads a chip amount from a BGR image region.

    Returns None if pytesseract is not installed, tesseract binary is missing,
    or the text cannot be parsed as a number.
    """

    def __init__(self) -> None:
        self._available = _PYTESSERACT_AVAILABLE
        if not self._available:
            print("ChipOcr: pytesseract not installed — pot odds disabled. "
                  "Run: pip install pytesseract")

    def read(self, bgr: np.ndarray) -> Optional[float]:
        """
        Extract a chip amount from a BGR image crop.

        Preprocesses: grayscale -> threshold -> 2x upscale for better OCR.
        Returns float value or None on failure.
        """
        if not self._available or bgr is None or bgr.size == 0:
            return None

        try:
            gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
            _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            upscaled = cv2.resize(thresh, None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR)

            text = pytesseract.image_to_string(upscaled, config=_TESSERACT_CONFIG).strip()
            cleaned = text.replace("$", "").replace(",", "").strip()
            return float(cleaned) if cleaned else None
        except Exception:
            return None
