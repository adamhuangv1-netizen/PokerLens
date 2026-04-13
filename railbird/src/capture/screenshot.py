"""
Screen capture utilities using mss.

NOTE: mss returns BGRA on Windows. All functions return BGR numpy arrays
(OpenCV convention) unless otherwise noted.
"""

import ctypes
import numpy as np
import mss
import mss.tools


def set_dpi_aware() -> None:
    """
    Call once at startup to fix coordinate mismatches caused by DPI scaling.
    Must be called before any window geometry queries.
    """
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(2)  # PROCESS_PER_MONITOR_DPI_AWARE
    except Exception:
        try:
            ctypes.windll.user32.SetProcessDPIAware()
        except Exception:
            pass


def grab_region(bbox: tuple[int, int, int, int]) -> np.ndarray:
    """
    Capture a screen region and return a BGR numpy array.

    Args:
        bbox: (left, top, width, height) in screen coordinates.

    Returns:
        np.ndarray of shape (height, width, 3), dtype uint8, BGR.
    """
    left, top, width, height = bbox
    monitor = {"left": left, "top": top, "width": width, "height": height}
    with mss.mss() as sct:
        raw = sct.grab(monitor)
    # mss returns BGRA; drop alpha channel to get BGR
    bgr = np.array(raw)[:, :, :3]
    return bgr


def grab_fullscreen(monitor_index: int = 1) -> np.ndarray:
    """
    Capture an entire monitor.

    Args:
        monitor_index: 1-based monitor index (0 = all monitors combined).

    Returns:
        np.ndarray of shape (height, width, 3), dtype uint8, BGR.
    """
    with mss.mss() as sct:
        monitor = sct.monitors[monitor_index]
        raw = sct.grab(monitor)
    return np.array(raw)[:, :, :3]


def list_monitors() -> list[dict]:
    """
    Return metadata for all available monitors.

    Returns:
        List of dicts with keys: left, top, width, height.
        Index 0 is the combined virtual screen; index 1+ are individual monitors.
    """
    with mss.mss() as sct:
        return list(sct.monitors)
