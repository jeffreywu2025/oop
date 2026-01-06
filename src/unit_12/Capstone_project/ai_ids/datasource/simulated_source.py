from __future__ import annotations

import threading
import time
from typing import Optional

from controller.event_bus import EventBus
from events.base import LoginEvent


class SimulatedDataSource:
    """
    Simple generator of login events to drive the IDS in demo mode.
    """

    def __init__(self, event_bus: EventBus, interval_sec: float = 0.5) -> None:
        self.event_bus = event_bus
        self.interval_sec = max(0.1, interval_sec)
        self._running = False
        self._thread: Optional[threading.Thread] = None
        self._toggle = False

    def start(self) -> None:
        if self._running:
            return
        self._running = True
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def stop(self) -> None:
        self._running = False
        if self._thread:
            self._thread.join(timeout=5.0)

    def _run(self) -> None:
        ip = "203.0.113.5"
        while self._running:
            ev = LoginEvent(
                username="alice",
                success=self._toggle,
                ip_address=ip,
            )
            self._toggle = not self._toggle
            self.event_bus.publish(ev)
            time.sleep(self.interval_sec)
