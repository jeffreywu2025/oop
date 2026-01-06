from __future__ import annotations

from datetime import timedelta
from typing import Optional, List

from controller.config import DetectionContext, DetectionResult
from detectors.base import Rule
from events.base import Event, LoginEvent, NetworkEvent


class FailedLoginBurstRule(Rule):
    """Detect multiple failed logins from same IP in a short time."""

    def __init__(self, threshold: int, window_sec: int) -> None:
        super().__init__("FailedLoginBurstRule")
        self.threshold = max(1, threshold)
        self.window_sec = max(1, window_sec)

    def match(self, event: Event, ctx: DetectionContext) -> Optional[DetectionResult]:
        if not isinstance(event, LoginEvent):
            return None
        if event.success:
            return None

        since = event.timestamp - timedelta(seconds=self.window_sec)
        recent = ctx.events_since(since)
        failed = [
            e
            for e in recent
            if isinstance(e, LoginEvent)
            and not e.success
            and e.ip_address == event.ip_address
        ]
        if len(failed) >= self.threshold:
            desc = (
                f"Detected {len(failed)} failed logins from IP {event.ip_address} "
                f"within {self.window_sec} seconds."
            )
            return DetectionResult(severity=8, description=desc, source_detector=self.name)
        return None

    def describe(self) -> str:
        return (
            f"Triggers when >= {self.threshold} failed logins occur "
            f"from same IP within {self.window_sec} seconds."
        )


class SuspiciousIPRule(Rule):
    """Detects events originating from blacklisted IP addresses.
    
    This rule triggers when any event (login, network, etc.) comes from
    an IP address that appears in the configured blacklist.
    """
    
    def __init__(self, blacklist: set[str]) -> None:
        super().__init__("SuspiciousIPRule")
        self.blacklist = blacklist

    def match(self, event: Event, ctx: DetectionContext) -> Optional[DetectionResult]:
        ip: Optional[str] = None
        if isinstance(event, LoginEvent):
            ip = event.ip_address
        elif isinstance(event, NetworkEvent):
            ip = event.src_ip

        if ip and ip in self.blacklist:
            desc = f"Event from blacklisted IP {ip}."
            return DetectionResult(severity=9, description=desc, source_detector=self.name)
        return None

    def describe(self) -> str:
        return "Triggers when event originates from a blacklisted IP address."


class EventFloodRule(Rule):
    """Detect too many events within a short time window (DoS-like flood)."""

    def __init__(self, max_events: int, window_sec: int) -> None:
        super().__init__("EventFloodRule")
        self.max_events = max(1, max_events)
        self.window_sec = max(1, window_sec)

    def match(self, event: Event, ctx: DetectionContext) -> Optional[DetectionResult]:
        since = event.timestamp - timedelta(seconds=self.window_sec)
        recent = ctx.events_since(since)
        if len(recent) >= self.max_events:
            desc = (
                f"{len(recent)} events received in last {self.window_sec} seconds "
                f"(threshold {self.max_events}). Possible event flood."
            )
            return DetectionResult(severity=7, description=desc, source_detector=self.name)
        return None

    def describe(self) -> str:
        return (
            f"Triggers when total events in last {self.window_sec} seconds exceed "
            f"{self.max_events}."
        )


class RuleBasedDetector:
    """Aggregates multiple detection rules into a single detector.
    
    This detector runs all configured rules against each event and
    collects any detection results produced by the individual rules.
    Enables combining multiple rule-based detection strategies.
    """

    def __init__(self, rules: List[Rule]) -> None:
        self.name = "RuleBasedDetector"
        self.rules = list(rules)

    def analyze(self, event: Event, ctx: DetectionContext) -> List[DetectionResult]:
        results: List[DetectionResult] = []
        for rule in self.rules:
            result = rule.match(event, ctx)
            if result:
                results.append(result)
        return results
