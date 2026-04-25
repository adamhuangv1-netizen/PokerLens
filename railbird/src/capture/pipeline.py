"""
CaptureLoop — the hot path that runs every frame.

Capture -> Crop -> Classify -> Emit results.

Target: run_once() completes in <50ms so the equity engine has budget remaining.
"""

import time
from dataclasses import dataclass
from typing import Callable, Optional

import numpy as np

from src.capture.cropper import TableProfile, crop_regions
from src.capture.window import capture_window, find_window, get_window_bbox
from src.common.constants import FOLDED_LABELS
from src.recognition.inference import CardRecognizer
from src.recognition.ocr import ChipOcr


@dataclass
class FrameResult:
    """Output of one capture cycle."""
    timestamp: float                          # time.perf_counter() at capture
    cards: dict[str, tuple[str, float]]       # region_key -> (label, confidence)
    window_found: bool
    elapsed_ms: float
    pot_amount: Optional[float] = None        # OCR'd pot total (None if not calibrated)
    to_call_amount: Optional[float] = None   # OCR'd to-call amount (None if not calibrated)

    @property
    def hero_cards(self) -> list[tuple[str, float]]:
        return [v for k, v in self.cards.items() if k.startswith("hero_")]

    @property
    def community_cards(self) -> list[tuple[str, float]]:
        return [v for k, v in self.cards.items()
                if k.startswith("flop_") or k in ("turn", "river")]

    def known_labels(self) -> dict[str, str]:
        """Return only regions with confident, non-empty, non-unknown labels."""
        return {k: v[0] for k, v in self.cards.items()
                if v[0] not in ("unknown", "empty", "back")}

    def count_active_opponents(self, seat_key_groups: list[list[str]]) -> int:
        """
        Count seats that appear to still be in the hand.

        A seat is active if any of its card regions shows a label that is NOT
        in FOLDED_LABELS — i.e. a real card label OR "back" (face-down but still
        in the hand). Only "empty" and "unknown" slots are treated as folded.

        Args:
            seat_key_groups: One list of region keys per seat (e.g.
                [["seat_1_card_1", "seat_1_card_2"], ["seat_2_card_1", ...]]).

        Returns:
            Number of active opponent seats (minimum 1 so equity is always valid).
        """
        count = 0
        for keys in seat_key_groups:
            if any(self.cards.get(k, ("empty", 0.0))[0] not in FOLDED_LABELS for k in keys):
                count += 1
        return max(1, count)


class CaptureLoop:
    """
    Runs capture -> crop -> classify for one poker table profile.

    Can be called manually (run_once) or run in a thread (run_forever).

    Example:
        loop = CaptureLoop(profile, recognizer)
        result = loop.run_once()
    """

    def __init__(
        self,
        profile: TableProfile,
        recognizer: CardRecognizer,
        on_result: Optional[Callable[[FrameResult], None]] = None,
    ) -> None:
        self._profile = profile
        self._recognizer = recognizer
        self._on_result = on_result
        self._hwnd: Optional[int] = None
        self._running = False
        self._ocr = ChipOcr() if (profile.pot_region or profile.to_call_region) else None

    def _ensure_window(self) -> bool:
        """Find the poker window if we don't have a handle yet. Returns True if found."""
        if self._hwnd is not None:
            # Verify still valid
            bbox = get_window_bbox(self._hwnd)
            if bbox and bbox[2] > 0:
                return True
            self._hwnd = None

        info = find_window(self._profile.window_title)
        if info:
            self._hwnd = info["hwnd"]
            return True
        return False

    def run_once(self) -> FrameResult:
        """
        Execute one capture-crop-classify cycle.

        Returns a FrameResult. If the poker window can't be found,
        returns a result with window_found=False and empty cards.
        """
        t0 = time.perf_counter()

        if not self._ensure_window():
            return FrameResult(
                timestamp=t0,
                cards={},
                window_found=False,
                elapsed_ms=0.0,
            )

        frame = capture_window(self._hwnd)
        if frame is None:
            self._hwnd = None
            return FrameResult(timestamp=t0, cards={}, window_found=False, elapsed_ms=0.0)

        crops = crop_regions(frame, self._profile)

        # Batch classify all regions in one ONNX call
        keys = list(crops.keys())
        images = [crops[k] for k in keys]

        if not images:
            return FrameResult(
                timestamp=t0,
                cards={},
                window_found=True,
                elapsed_ms=(time.perf_counter() - t0) * 1000,
            )

        predictions = self._recognizer.predict_batch(images)

        cards = {key: pred for key, pred in zip(keys, predictions)}

        # OCR pot and to-call amounts if regions are calibrated
        pot_amount = None
        to_call_amount = None
        if self._ocr is not None:
            h, w = frame.shape[:2]
            if self._profile.pot_region:
                x, y, rw, rh = self._profile.pot_region.to_pixels(w, h)
                pot_crop = frame[y:y+rh, x:x+rw]
                pot_amount = self._ocr.read(pot_crop)
            if self._profile.to_call_region:
                x, y, rw, rh = self._profile.to_call_region.to_pixels(w, h)
                call_crop = frame[y:y+rh, x:x+rw]
                to_call_amount = self._ocr.read(call_crop)

        elapsed = (time.perf_counter() - t0) * 1000

        result = FrameResult(
            timestamp=t0,
            cards=cards,
            window_found=True,
            elapsed_ms=elapsed,
            pot_amount=pot_amount,
            to_call_amount=to_call_amount,
        )

        if self._on_result:
            self._on_result(result)

        return result

    def run_forever(self, interval_ms: float = 100.0) -> None:
        """
        Run in a loop, calling run_once() and sleeping to maintain interval_ms cadence.
        Blocks the calling thread. Call stop() from another thread to exit.
        """
        self._running = True
        while self._running:
            t_start = time.perf_counter()
            self.run_once()
            elapsed = (time.perf_counter() - t_start) * 1000
            sleep_ms = max(0.0, interval_ms - elapsed)
            if sleep_ms > 0:
                time.sleep(sleep_ms / 1000.0)

    def stop(self) -> None:
        self._running = False
