"""
PokerLens — main entry point.

Wires together:
  CaptureLoop (QThread)  ->  EquityCalculator  ->  OverlayWindow
                                                 ->  HandTracker  ->  PokerDB

Usage:
    python main.py --profile config/site_profiles/my_table.json
    python main.py --profile config/site_profiles/my_table.json --opponents 3
    python main.py --profile config/site_profiles/my_table.json --debug

Controls:
    F12  — toggle overlay visibility
    The app runs until the window is closed via the system tray (or Ctrl+C in terminal).
"""

import argparse
import os
import sys
import time
import threading
from typing import Optional

# Must set DPI awareness before any Qt or ctypes window calls
from src.capture.screenshot import set_dpi_aware
set_dpi_aware()

from PyQt6.QtCore import Qt, QThread, QTimer, pyqtSignal, QObject
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication, QMenu, QSystemTrayIcon

from src.capture.cropper import load_profile, TableProfile
from src.capture.pipeline import CaptureLoop, FrameResult
from src.capture.window import find_window, get_window_bbox
from src.engine.equity import EquityCalculator
from src.engine.strategy import advise
from src.overlay.widget import OverlayWindow
from src.recognition.inference import CardRecognizer
from src.tracking.database import PokerDB
from src.tracking.hand_tracker import HandTracker
from src.tracking.stats import compute_all_stats
from src.capture.log_tailer import LogTailer


class CaptureWorker(QObject):
    """Runs CaptureLoop in a QThread, emits results via signal."""
    frame_ready = pyqtSignal(object)  # FrameResult

    def __init__(self, loop: CaptureLoop, interval_ms: float = 100.0) -> None:
        super().__init__()
        self._loop = loop
        self._interval = interval_ms
        self._running = False

    def run(self) -> None:
        self._running = True
        while self._running:
            t0 = time.perf_counter()
            result = self._loop.run_once()
            self.frame_ready.emit(result)
            elapsed = (time.perf_counter() - t0) * 1000
            sleep_ms = max(0.0, self._interval - elapsed)
            if sleep_ms > 0:
                time.sleep(sleep_ms / 1000.0)

    def stop(self) -> None:
        self._running = False


class PokerLensApp:
    """Main application controller."""

    def __init__(
        self,
        profile: TableProfile,
        num_opponents: int = 1,
        debug: bool = False,
    ) -> None:
        self._profile = profile
        self._num_opponents = num_opponents
        self._debug = debug

        # --- Core components ---
        self._recognizer = CardRecognizer()
        self._equity_calc = EquityCalculator()
        self._db = PokerDB()
        self._db.start_session(profile.name)

        seat_keys = [r.key for r in profile.seat_cards]
        self._hand_tracker = HandTracker(self._db, seat_keys)

        # --- Capture loop (worker thread) ---
        capture_loop = CaptureLoop(profile, self._recognizer)
        self._worker = CaptureWorker(capture_loop)
        self._capture_thread = QThread()
        self._worker.moveToThread(self._capture_thread)
        self._capture_thread.started.connect(self._worker.run)
        self._worker.frame_ready.connect(self._on_frame)

        # --- Log Tailer ---
        self._log_tailer = LogTailer(
            directory=os.path.join(os.environ.get("LOCALAPPDATA", ""), "PokerStars", "HandHistory"),
            on_hand_parsed=self._hand_tracker.on_parsed_hand
        )
        self._log_tailer.start()

        # --- Overlay ---
        win_info = find_window(profile.window_title)
        if win_info:
            bx, by, bw, bh = win_info["bbox"]
            ov_x, ov_y, ov_w, ov_h = bx, by, bw, bh
        else:
            screen = QApplication.primaryScreen().geometry()
            ov_x, ov_y, ov_w, ov_h = screen.x(), screen.y(), screen.width(), screen.height()

        self._overlay = OverlayWindow(ov_x, ov_y, ov_w, ov_h, profile)
        self._overlay.show()

        # --- Global hotkey for F12 toggle ---
        self._setup_hotkey()

        # --- DB flush timer (every 10 seconds) ---
        self._flush_timer = QTimer()
        self._flush_timer.setInterval(10_000)
        self._flush_timer.timeout.connect(self._db.flush)
        self._flush_timer.start()

        # --- Equity runs in a thread to avoid blocking GUI ---
        self._equity_thread_running = False

        # --- System tray ---
        self._tray = self._build_tray()

    def start(self) -> None:
        self._capture_thread.start()

    def _on_frame(self, result: FrameResult) -> None:
        """Called on main thread when a new frame is ready."""
        if not result.window_found:
            self._overlay.update_display([], [], waiting=True)
            return

        # Update hand tracker (very fast, ~1ms)
        self._hand_tracker.update(result)

        # Extract card labels
        hero_labels = [label for label, conf in result.hero_cards]
        board_labels = [label for label, conf in result.community_cards]

        # Compute equity in a background thread to keep UI responsive
        threading.Thread(
            target=self._compute_and_update,
            args=(hero_labels, board_labels, result.elapsed_ms),
            daemon=True,
        ).start()

        # Flush DB periodically (non-blocking since it checks pending count)
        if len(self._db._pending) >= 10:
            threading.Thread(target=self._db.flush, daemon=True).start()

    def _compute_and_update(
        self,
        hero_labels: list[str],
        board_labels: list[str],
        capture_ms: float,
    ) -> None:
        """Run equity calculation and update overlay. Runs in a daemon thread."""
        t0 = time.perf_counter()

        equity_result = None
        advice_result = None

        valid_hero = [l for l in hero_labels if l not in ("unknown", "empty", "back")]
        if len(valid_hero) == 2:
            try:
                equity_result = self._equity_calc.calculate(
                    hero=valid_hero,
                    board=board_labels,
                    num_opponents=self._num_opponents,
                )
                if equity_result:
                    advice_result = advise(equity_result)
            except Exception as e:
                if self._debug:
                    print(f"Equity error: {e}")
                    
        # Grab stats
        all_stats = compute_all_stats(self._db, list({seat.rsplit("_card", 1)[0] for seat in self._hand_tracker._seats.keys()}))

        total_ms = capture_ms + (time.perf_counter() - t0) * 1000

        # Use QTimer.singleShot to safely update the GUI from this background thread
        QTimer.singleShot(0, lambda: self._overlay.update_display(
            hero_labels=hero_labels,
            board_labels=board_labels,
            equity_result=equity_result,
            advice=advice_result,
            latency_ms=total_ms if self._debug else None,
            waiting=(len(valid_hero) < 2),
            seat_stats=all_stats
        ))

    def _reposition_overlay(self) -> None:
        """Re-align the overlay to the poker window position."""
        info = find_window(self._profile.window_title)
        if info:
            bx, by, bw, bh = info["bbox"]
            self._overlay.reposition(bx, by, bw, 70)

    def _setup_hotkey(self) -> None:
        """Register F12 as a global hotkey to toggle overlay visibility."""
        try:
            from pynput import keyboard

            def _on_press(key):
                if key == keyboard.Key.f12:
                    # Must call Qt methods on the main thread
                    QTimer.singleShot(0, self._overlay.toggle_visible)

            listener = keyboard.Listener(on_press=_on_press)
            listener.daemon = True
            listener.start()
        except ImportError:
            print("pynput not installed — F12 hotkey disabled.")

    def _build_tray(self) -> Optional[QSystemTrayIcon]:
        """Build a system tray icon with basic controls."""
        try:
            tray = QSystemTrayIcon()
            tray.setToolTip("PokerLens")
            menu = QMenu()

            toggle_action = menu.addAction("Toggle Overlay (F12)")
            toggle_action.triggered.connect(self._overlay.toggle_visible)

            reposition_action = menu.addAction("Reposition Overlay")
            reposition_action.triggered.connect(self._reposition_overlay)

            menu.addSeparator()
            quit_action = menu.addAction("Quit PokerLens")
            quit_action.triggered.connect(QApplication.quit)

            tray.setContextMenu(menu)
            tray.show()
            return tray
        except Exception:
            return None

    def shutdown(self) -> None:
        self._worker.stop()
        self._log_tailer.stop()
        self._capture_thread.quit()
        self._capture_thread.wait(2000)
        self._flush_timer.stop()
        self._db.close()


def main() -> None:
    parser = argparse.ArgumentParser(description="PokerLens — real-time poker overlay")
    parser.add_argument("--profile", required=True,
                        help="Path to a calibrated table profile JSON")
    parser.add_argument("--opponents", type=int, default=1,
                        help="Number of active opponents (default: 1)")
    parser.add_argument("--debug", action="store_true",
                        help="Show pipeline latency in HUD")
    args = parser.parse_args()

    if not os.path.exists(args.profile):
        print(f"Profile not found: {args.profile}")
        print("Run: python scripts/calibrate.py --window <title> --profile-name <name>")
        sys.exit(1)

    profile = load_profile(args.profile)
    print(f"Loaded profile: {profile.name} (window: '{profile.window_title}')")
    print(f"  Hero cards:      {len(profile.hero_cards)}")
    print(f"  Community cards: {len(profile.community_cards)}")
    print(f"  Seat cards:      {len(profile.seat_cards)}")

    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)  # Keep running when overlay is hidden

    poker_app = PokerLensApp(profile, num_opponents=args.opponents, debug=args.debug)
    poker_app.start()

    print("\nPokerLens running. Press F12 to toggle overlay. Right-click tray icon to quit.")
    ret = app.exec()
    poker_app.shutdown()
    sys.exit(ret)


if __name__ == "__main__":
    main()
