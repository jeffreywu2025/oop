from __future__ import annotations

import logging
from pathlib import Path
from typing import Iterable

from controller.event_bus import EventBus
from events.base import LoginEvent

logger = logging.getLogger("IDS.datasource")


class LogFileDataSource:
    """
    Very simple log file parser.
    Expected format per line:
        login,username,success,ip
    e.g.:
        login,alice,0,203.0.113.5
    """

    def __init__(self, event_bus: EventBus, file_path: str) -> None:
        self.event_bus = event_bus
        self.file_path = Path(file_path)

    def replay(self) -> None:
        if not self.file_path.exists():
            logger.error("Log file not found: %s", self.file_path)
            return

        for line in self._safe_read_lines():
            parts = [p.strip() for p in line.split(",")]
            if len(parts) < 4:
                continue
            record_type, username, success_str, ip = parts[:4]
            if record_type != "login":
                continue
            success = success_str == "1"
            ev = LoginEvent(username=username, success=success, ip_address=ip)
            self.event_bus.publish(ev)

    def _safe_read_lines(self) -> Iterable[str]:
        try:
            with self.file_path.open("r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        yield line
        except OSError as e:
            logger.error("Error reading log file: %s", e)
