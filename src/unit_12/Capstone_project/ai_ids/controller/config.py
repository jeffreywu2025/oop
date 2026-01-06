from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import List

from events.base import Event


@dataclass
class SecurityConfig:
    """Configuration settings for the intrusion detection system.
    
    Contains all tunable parameters for detection thresholds, time windows,
    blacklists, and other security-related configuration values.
    """
    
    blacklisted_ips: set[str] = field(default_factory=set)
    max_failed_login_per_minute: int = 5
    event_flood_threshold: int = 100
    event_flood_window_sec: int = 10
    anomaly_threshold: float = 0.8  # 0–1 scale


@dataclass
class DetectionResult:
    """Represents the result of a security threat detection.
    
    Contains the threat severity level, human-readable description,
    and identification of the detector that generated the result.
    """
    
    severity: int  # 1–10
    description: str
    source_detector: str


@dataclass
class DetectionContext:
    """Provides context information for threat detection analysis.
    
    Maintains a sliding window of recent events and system configuration
    to enable detectors to analyze patterns and make informed decisions.
    """
    
    recent_events: List[Event] = field(default_factory=list)
    config: SecurityConfig = field(default_factory=SecurityConfig)

    def add_event(self, event: Event, max_events: int = 1000) -> None:
        self.recent_events.append(event)
        if len(self.recent_events) > max_events:
            self.recent_events.pop(0)

    def events_since(self, since: datetime) -> List[Event]:
        return [e for e in self.recent_events if e.timestamp >= since]
