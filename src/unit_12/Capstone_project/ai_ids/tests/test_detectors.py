from __future__ import annotations

from datetime import datetime, timedelta, timezone

from controller.config import DetectionContext, SecurityConfig
from detectors.rules import FailedLoginBurstRule, SuspiciousIPRule
from events.base import LoginEvent


def test_failed_login_burst_triggers():
    config = SecurityConfig()
    ctx = DetectionContext(config=config)

    base_time = datetime.now(timezone.utc)
    ip = "203.0.113.5"

    # Add two previous failed logins
    for i in range(2):
        e = LoginEvent(
            username="alice",
            success=False,
            ip_address=ip,
            timestamp=base_time - timedelta(seconds=5 - i),
        )
        ctx.add_event(e)

    rule = FailedLoginBurstRule(threshold=3, window_sec=10)
    event = LoginEvent(
        username="alice",
        success=False,
        ip_address=ip,
        timestamp=base_time,
    )
    # Add current event to context first (as IDSController does)
    ctx.add_event(event)
    result = rule.match(event, ctx)
    assert result is not None
    assert result.severity >= 1


def test_suspicious_ip_rule():
    blacklisted = {"198.51.100.10"}
    config = SecurityConfig(blacklisted_ips=blacklisted)
    ctx = DetectionContext(config=config)

    event = LoginEvent(
        username="bob",
        success=True,
        ip_address="198.51.100.10",
    )
    rule = SuspiciousIPRule(blacklist=blacklisted)
    result = rule.match(event, ctx)
    assert result is not None
    assert "blacklisted" in result.description
