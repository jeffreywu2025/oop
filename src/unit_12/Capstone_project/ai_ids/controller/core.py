from __future__ import annotations

import logging
import threading
from typing import List

from actions.actions import Action
from controller.config import DetectionContext, DetectionResult, SecurityConfig
from events.base import Event
from detectors.base import Detector  # type: ignore[import]

logger = logging.getLogger("IDS.controller")


class IDSController:
    """
    Core IDS orchestrator.
    EventBus calls consume() in a single worker thread => simplified thread safety.
    """

    def __init__(self, config: SecurityConfig | None = None) -> None:
        self.config = config or SecurityConfig()
        self.ctx = DetectionContext(config=self.config)
        self.detectors: List[Detector] = []
        self.actions: List[Action] = []
        self._lock = threading.Lock()

    def add_detector(self, detector: Detector) -> None:
        with self._lock:
            self.detectors.append(detector)

    def add_action(self, action: Action) -> None:
        with self._lock:
            self.actions.append(action)

    def consume(self, event: Event) -> None:
        if not isinstance(event, Event):
            logger.error("Invalid event type passed to IDSController.consume: %r", type(event))
            return

        with self._lock:
            self.ctx.add_event(event)
            results: List[DetectionResult] = []
            for det in self.detectors:
                try:
                    results.extend(det.analyze(event, self.ctx))
                except Exception as e:
                    logger.exception("Detector %s failed: %s", getattr(det, "name", "?"), e)

            for result in results:
                for action in self.actions:
                    try:
                        action.execute(result, event, self.ctx)
                    except Exception as e:
                        logger.exception("Action %s failed: %s", action.name, e)
