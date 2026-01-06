from __future__ import annotations

from controller.config import DetectionContext, DetectionResult, SecurityConfig
from actions.actions import EmailAlertAction
from events.base import LoginEvent


def test_email_alert_action_uses_sender():
    # Arrange
    config = SecurityConfig()
    ctx = DetectionContext(config=config)
    event = LoginEvent(username="alice", success=False, ip_address="203.0.113.5")

    result = DetectionResult(
        severity=9,
        description="Test high severity alert",
        source_detector="UnitTestDetector",
    )

    outbox: list[tuple[str, str]] = []

    def fake_sender(subject: str, body: str) -> None:
        outbox.append((subject, body))

    action = EmailAlertAction(recipient="security@example.com", sender=fake_sender)

    # Act
    action.execute(result, event, ctx)

    # Assert
    assert len(outbox) == 1
    subject, body = outbox[0]
    assert "Severity 9" in subject
    assert "Test high severity alert" in body
