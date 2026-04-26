"""
WsReader — receives poker state from the PokerLens Chrome extension via WebSocket.

The browser extension (railbird/extension/) connects to ws://localhost:9234 and
pushes card state every 200ms. This reader exposes the same run_once() interface
as CaptureLoop so main.py can swap between them transparently.

No special Chrome launch flags required — install the extension in your normal browser.
"""

import asyncio
import json
import threading
import time
from typing import Optional

from src.capture.pipeline import FrameResult

_COMMUNITY_KEYS = ["flop_1", "flop_2", "flop_3", "turn", "river"]

_WS_PORT = 9234


class DomReader:
    """
    WebSocket server that receives card state from the PokerLens Chrome extension.

    Call start() once, then poll run_once() in a loop.
    """

    def __init__(self, url: str, port: int = _WS_PORT) -> None:
        self._url = url  # kept for compatibility; not used at runtime
        self._port = port
        self._state: dict = {}
        self._lock = threading.Lock()
        self._thread: Optional[threading.Thread] = None
        self._loop: Optional[asyncio.AbstractEventLoop] = None
        self._connected = False

    def connect(self) -> bool:
        """Start the WebSocket server in a background thread. Always succeeds."""
        self._thread = threading.Thread(target=self._run_server, daemon=True)
        self._thread.start()
        print(f"PokerLens WebSocket server listening on ws://localhost:{self._port}")
        print("Make sure the PokerLens Chrome extension is installed and active on Poker Patio.")
        return True

    # ------------------------------------------------------------------ server

    def _run_server(self) -> None:
        self._loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self._loop)
        self._loop.run_until_complete(self._serve())

    async def _serve(self) -> None:
        try:
            import websockets
        except ImportError:
            print("websockets not installed — run: pip install websockets")
            return

        async def handler(websocket):
            self._connected = True
            try:
                async for message in websocket:
                    try:
                        data = json.loads(message)
                        with self._lock:
                            self._state = data
                    except Exception:
                        pass
            finally:
                self._connected = False

        async with websockets.serve(handler, "localhost", self._port):
            await asyncio.Future()  # run forever

    # ---------------------------------------------------------------- run_once

    def run_once(self) -> FrameResult:
        t0 = time.perf_counter()

        with self._lock:
            data = dict(self._state)

        if not data:
            # No message received yet — extension not connected
            return FrameResult(timestamp=t0, cards={}, window_found=False, elapsed_ms=0.0)

        hero: list[str] = data.get("hero", [])
        community: list[str] = data.get("community", [])

        cards: dict[str, tuple[str, float]] = {}
        for i, key in enumerate(("hero_1", "hero_2")):
            cards[key] = (hero[i], 1.0) if i < len(hero) else ("empty", 1.0)
        for i, key in enumerate(_COMMUNITY_KEYS):
            cards[key] = (community[i], 1.0) if i < len(community) else ("empty", 1.0)

        elapsed = (time.perf_counter() - t0) * 1000
        return FrameResult(
            timestamp=t0,
            cards=cards,
            window_found=True,
            elapsed_ms=elapsed,
            pot_amount=data.get("pot"),
            to_call_amount=data.get("toCall"),
            active_opponents=max(1, data.get("activeOpp") or 1),
        )

    def stop(self) -> None:
        if self._loop:
            self._loop.call_soon_threadsafe(self._loop.stop)
