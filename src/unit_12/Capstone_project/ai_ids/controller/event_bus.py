from __future__ import annotations

import logging
import queue
import threading
from typing import List, Optional, Protocol

from events.base import Event

logger = logging.getLogger("IDS.event_bus")


class EventConsumer(Protocol):
    """Protocol defining the interface for event consumers.
    
    Components that need to receive and process events from the event bus
    must implement this protocol's consume method.
    """
    
    def consume(self, event: Event) -> None: ...


class EventBus:
    """
    Thread-safe event bus with a single worker thread.
    Single consumer thread => simplified locking, minimal deadlock risk.
    """

    def __init__(self) -> None:
        self._queue: "queue.Queue[Event | None]" = queue.Queue()
        self._subscribers: List[EventConsumer] = []
        self._lock = threading.Lock()
        self._running = False
        self._worker_thread: Optional[threading.Thread] = None

    def subscribe(self, consumer: EventConsumer) -> None:
        with self._lock:
            if consumer not in self._subscribers:
                self._subscribers.append(consumer)

    def publish(self, event: Event) -> None:
        if not isinstance(event, Event):
            logger.error("Invalid event published: %r", type(event))
            return
        self._queue.put(event)

    def start(self) -> None:
        with self._lock:
            if self._running:
                return
            self._running = True
            self._worker_thread = threading.Thread(target=self._run, daemon=True)
            self._worker_thread.start()

    def stop(self) -> None:
        with self._lock:
            self._running = False
        self._queue.put(None)
        if self._worker_thread:
            self._worker_thread.join(timeout=5.0)

    def _run(self) -> None:
        while True:
            try:
                event = self._queue.get()
                if event is None:
                    break
                with self._lock:
                    subs = list(self._subscribers)
                for sub in subs:
                    try:
                        sub.consume(event)
                    except Exception as e:
                        logger.exception("Error in subscriber.consume: %s", e)
            except Exception as e:
                logger.exception("Error in EventBus worker: %s", e)
