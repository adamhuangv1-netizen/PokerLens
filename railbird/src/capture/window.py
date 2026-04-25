"""
Window discovery and capture utilities (Windows-specific).

Finds a poker client window by title substring and captures its contents.
"""

import ctypes
import ctypes.wintypes
import sys
from typing import Optional

import numpy as np
import mss

from src.capture.screenshot import grab_region


def _enumerate_windows(user32, title_filter: Optional[str] = None) -> list[dict]:
    """Return all visible windows with non-empty titles and positive dimensions.

    Args:
        title_filter: If provided, only windows whose title contains this string
                      (case-insensitive) are returned.
    """
    results = []

    def _callback(hwnd, _):
        if not user32.IsWindowVisible(hwnd):
            return True
        length = user32.GetWindowTextLengthW(hwnd)
        if length == 0:
            return True
        buf = ctypes.create_unicode_buffer(length + 1)
        user32.GetWindowTextW(hwnd, buf, length + 1)
        title = buf.value
        if title_filter is not None and title_filter.lower() not in title.lower():
            return True
        rect = ctypes.wintypes.RECT()
        user32.GetWindowRect(hwnd, ctypes.byref(rect))
        w = rect.right - rect.left
        h = rect.bottom - rect.top
        if w > 0 and h > 0:
            results.append({"hwnd": hwnd, "title": title, "bbox": (rect.left, rect.top, w, h)})
        return True

    EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.wintypes.HWND, ctypes.wintypes.LPARAM)
    user32.EnumWindows(EnumWindowsProc(_callback), 0)
    return results


def find_window(title_substring: str) -> Optional[dict]:
    """
    Find the visible window whose title contains `title_substring` (case-insensitive).
    When multiple windows match, returns the one with the largest area (the game table,
    not an auxiliary chat or notification window).

    Returns:
        dict with keys: hwnd (int), title (str), bbox (left, top, width, height)
        or None if not found.
    """
    if sys.platform != "win32":
        raise RuntimeError("Window discovery is only supported on Windows.")
    results = _enumerate_windows(ctypes.windll.user32, title_filter=title_substring)
    if not results:
        return None
    return max(results, key=lambda r: r["bbox"][2] * r["bbox"][3])


def list_windows() -> list[dict]:
    """Return all visible windows with non-empty titles."""
    if sys.platform != "win32":
        return []
    return _enumerate_windows(ctypes.windll.user32)


def capture_window(hwnd: int) -> Optional[np.ndarray]:
    """
    Capture a window's current on-screen position.

    NOTE: mss captures the screen bitmap at the window's bounding box.
    The window must be unobstructed for accurate results.

    Returns:
        BGR numpy array or None if the window can no longer be found.
    """
    if sys.platform != "win32":
        return None

    user32 = ctypes.windll.user32
    rect = ctypes.wintypes.RECT()
    if not user32.GetWindowRect(hwnd, ctypes.byref(rect)):
        return None

    w = rect.right - rect.left
    h = rect.bottom - rect.top
    if w <= 0 or h <= 0:
        return None
    # Minimized windows report left/top ≈ -32000
    if rect.left < -30000 or rect.top < -30000:
        return None

    return grab_region((rect.left, rect.top, w, h))


def get_window_bbox(hwnd: int) -> Optional[tuple[int, int, int, int]]:
    """Return current (left, top, width, height) for a window handle."""
    if sys.platform != "win32":
        return None
    user32 = ctypes.windll.user32
    rect = ctypes.wintypes.RECT()
    if not user32.GetWindowRect(hwnd, ctypes.byref(rect)):
        return None
    return (rect.left, rect.top, rect.right - rect.left, rect.bottom - rect.top)
