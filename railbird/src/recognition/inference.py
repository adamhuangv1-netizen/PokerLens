"""
ONNX Runtime inference wrapper for card classification.

Provides CardRecognizer — the single inference interface used by the
capture pipeline. Operates on BGR numpy arrays (OpenCV convention).
"""

import json
import os
from typing import Optional

import cv2
import numpy as np
import onnxruntime as ort

from src.common.constants import IDX_TO_LABEL, NUM_CLASSES

CARD_SIZE = (64, 64)
DEFAULT_MODEL_PATH = os.path.join(
    os.path.dirname(__file__), "..", "..", "data", "models", "card_classifier.onnx"
)
DEFAULT_NORM_STATS_PATH = os.path.join(
    os.path.dirname(__file__), "..", "..", "data", "models", "norm_stats.json"
)
DEFAULT_CONFIDENCE_THRESHOLD = 0.85


class CardRecognizer:
    """
    Loads an ONNX card classifier and provides fast CPU inference.

    Usage:
        recognizer = CardRecognizer()
        label, confidence = recognizer.predict(bgr_image)
        results = recognizer.predict_batch([img1, img2, img3])
    """

    def __init__(
        self,
        model_path: str = DEFAULT_MODEL_PATH,
        norm_stats_path: str = DEFAULT_NORM_STATS_PATH,
        confidence_threshold: float = DEFAULT_CONFIDENCE_THRESHOLD,
    ) -> None:
        if not os.path.exists(model_path):
            raise FileNotFoundError(
                f"ONNX model not found at {model_path}. Run train.py first."
            )

        sess_options = ort.SessionOptions()
        sess_options.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL
        sess_options.intra_op_num_threads = 2  # Limit CPU threads for latency

        self._session = ort.InferenceSession(
            model_path,
            sess_options=sess_options,
            providers=["CPUExecutionProvider"],
        )
        self._input_name = self._session.get_inputs()[0].name
        self._threshold = confidence_threshold

        # Load normalization stats
        self._mean, self._std = self._load_norm_stats(norm_stats_path)

    def _load_norm_stats(self, path: str) -> tuple[np.ndarray, np.ndarray]:
        if os.path.exists(path):
            with open(path) as f:
                d = json.load(f)
            mean = np.array(d["mean"], dtype=np.float32).reshape(3, 1, 1)
            std = np.array(d["std"], dtype=np.float32).reshape(3, 1, 1)
        else:
            # ImageNet defaults as fallback
            mean = np.array([0.485, 0.456, 0.406], dtype=np.float32).reshape(3, 1, 1)
            std = np.array([0.229, 0.224, 0.225], dtype=np.float32).reshape(3, 1, 1)
        return mean, std

    def _preprocess(self, bgr: np.ndarray) -> np.ndarray:
        """BGR uint8 -> normalized float32 tensor (1, 3, 64, 64)."""
        # Resize
        resized = cv2.resize(bgr, CARD_SIZE, interpolation=cv2.INTER_AREA)
        # BGR -> RGB, HWC -> CHW, uint8 -> float32 [0, 1]
        rgb = resized[:, :, ::-1].astype(np.float32) / 255.0
        chw = rgb.transpose(2, 0, 1)
        # Normalize
        normalized = (chw - self._mean) / self._std
        return normalized[np.newaxis].astype(np.float32)  # (1, 3, 64, 64)

    def _preprocess_batch(self, images: list[np.ndarray]) -> np.ndarray:
        """Preprocess a list of BGR images into a batched tensor."""
        return np.concatenate([self._preprocess(img) for img in images], axis=0)

    def predict(self, image: np.ndarray) -> tuple[str, float]:
        """
        Classify a single card image.

        Args:
            image: BGR numpy array (any size, will be resized to 64x64).

        Returns:
            (label, confidence) where label is from CARD_LABELS.
            Returns ("unknown", 0.0) if confidence < threshold.
        """
        tensor = self._preprocess(image)
        logits = self._session.run(None, {self._input_name: tensor})[0]  # (1, 54)
        probs = _softmax(logits[0])
        idx = int(np.argmax(probs))
        confidence = float(probs[idx])

        if confidence < self._threshold:
            return "unknown", confidence

        return IDX_TO_LABEL[idx], confidence

    def predict_batch(self, images: list[np.ndarray]) -> list[tuple[str, float]]:
        """
        Classify multiple card images in one forward pass.

        Args:
            images: List of BGR numpy arrays.

        Returns:
            List of (label, confidence) tuples in the same order.
        """
        if not images:
            return []

        batch = self._preprocess_batch(images)
        logits = self._session.run(None, {self._input_name: batch})[0]  # (N, 54)
        results = []
        for row in logits:
            probs = _softmax(row)
            idx = int(np.argmax(probs))
            confidence = float(probs[idx])
            if confidence < self._threshold:
                results.append(("unknown", confidence))
            else:
                results.append((IDX_TO_LABEL[idx], confidence))
        return results

    @property
    def confidence_threshold(self) -> float:
        return self._threshold

    @confidence_threshold.setter
    def confidence_threshold(self, value: float) -> None:
        self._threshold = value


def _softmax(x: np.ndarray) -> np.ndarray:
    e = np.exp(x - x.max())
    return e / e.sum()


def benchmark(model_path: str = DEFAULT_MODEL_PATH, n: int = 100) -> None:
    """Print inference latency stats over n random images."""
    import time
    recognizer = CardRecognizer(model_path)
    dummy = np.random.randint(0, 255, (200, 200, 3), dtype=np.uint8)

    # Warmup
    for _ in range(5):
        recognizer.predict(dummy)

    times = []
    for _ in range(n):
        t0 = time.perf_counter()
        recognizer.predict(dummy)
        times.append((time.perf_counter() - t0) * 1000)

    times.sort()
    print(f"Inference latency over {n} runs:")
    print(f"  median: {times[n // 2]:.2f}ms")
    print(f"  p95:    {times[int(n * 0.95)]:.2f}ms")
    print(f"  max:    {times[-1]:.2f}ms")


if __name__ == "__main__":
    benchmark()
