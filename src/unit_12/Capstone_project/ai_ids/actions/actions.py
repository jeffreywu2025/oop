from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from typing import Callable, Optional

from controller.config import DetectionContext, DetectionResult
from events.base import Event, LoginEvent, NetworkEvent

logger = logging.getLogger("IDS.actions")


class Action(ABC):
    """Abstract base class for security response actions.
    
    Defines the interface for actions that can be triggered when
    security threats are detected. All action implementations must
    inherit from this class and implement the execute method.
    """
    
    def __init__(self, name: str) -> None:
        self.name = name

    @abstractmethod
    def execute(self, result: DetectionResult, event: Event, ctx: DetectionContext) -> None:
        ...


class AlertAction(Action):
    """Generates warning-level log alerts for detected security events.
    
    This action creates high-visibility log entries when threats are detected,
    including the full detection details and original event information.
    """
    
    def __init__(self) -> None:
        super().__init__("AlertAction")

    def execute(self, result: DetectionResult, event: Event, ctx: DetectionContext) -> None:
        logger.warning(
            "ALERT: %s (severity=%d) | event=%s",
            result.description,
            result.severity,
            event.to_dict(),
        )


class BlockIPAction(Action):
    """Simulate IP blocking by adding it to blacklist."""

    def __init__(self) -> None:
        super().__init__("BlockIPAction")

    def execute(self, result: DetectionResult, event: Event, ctx: DetectionContext) -> None:
        ip = None
        if isinstance(event, LoginEvent):
            ip = event.ip_address
        elif isinstance(event, NetworkEvent):
            ip = event.src_ip

        if ip:
            ctx.config.blacklisted_ips.add(ip)
            logger.info("Blocking IP %s due to detection: %s", ip, result.description)


class LogAction(Action):
    """Records security events to the application log.
    
    Creates structured log entries for all detected security events,
    providing an audit trail for security incidents and analysis.
    """
    
    def __init__(self) -> None:
        super().__init__("LogAction")

    def execute(self, result: DetectionResult, event: Event, ctx: DetectionContext) -> None:
        logger.info(
            "SECURITY EVENT: detector=%s, severity=%d, desc=%s",
            result.source_detector,
            result.severity,
            result.description,
        )


class EmailAlertAction(Action):
    """
    Email-style alert action.

    For security and simplicity, this does NOT send real emails.
    Instead, it calls an injected 'sender' function.
    In production, that function could wrap smtplib, an API, etc.
    In tests, we inject a fake sender and assert it was called.
    """

    def __init__(
        self,
        recipient: str,
        sender: Optional[Callable[[str, str], None]] = None,
    ) -> None:
        super().__init__("EmailAlertAction")
        self.recipient = recipient
        self._sender = sender or self._default_sender

    def _default_sender(self, subject: str, body: str) -> None:
        # In a real system this could send via SMTP; here we only log.
        logger.warning(
            "EMAIL ALERT to %s | subject=%s | body=%s",
            self.recipient,
            subject,
            body,
        )

    def execute(self, result: DetectionResult, event: Event, ctx: DetectionContext) -> None:
        subject = f"[IDS] Severity {result.severity} alert from {result.source_detector}"
        body = result.description
        self._sender(subject, body)
