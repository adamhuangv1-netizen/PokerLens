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
from src.recognition.inference import CardRecognizer


@dataclass
class FrameResult:
    """Output of one capture cycle."""
    timestamp: float                          # time.perf_counter() at capture
    cards: dict[str, tuple[str, float]]       # region_key -> (label, confidence)
    window_found: bool
    elapsed_ms: float

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
        elapsed = (time.perf_counter() - t0) * 1000

        result = FrameResult(
            timestamp=t0,
            cards=cards,
            window_found=True,
            elapsed_ms=elapsed,
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
