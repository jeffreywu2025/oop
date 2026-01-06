from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime, timezone
from typing import Dict, Optional


class Event(ABC):
    """Base security event."""

    def __init__(self, source: str, timestamp: Optional[datetime] = None) -> None:
        self.source = source
        self.timestamp = timestamp or datetime.now(timezone.utc)

    @abstractmethod
    def to_dict(self) -> Dict:
        return {
            "source": self.source,
            "timestamp": self.timestamp.isoformat(),
        }


class LoginEvent(Event):
    """Represents a user login attempt event.

    This event captures authentication attempts including both successful
    and failed login attempts along with the source IP address.
    """

    def __init__(
        self,
        username: str,
        success: bool,
        ip_address: str,
        source: str = "auth_service",
        timestamp: Optional[datetime] = None,
    ) -> None:
        super().__init__(source, timestamp)
        self.username = username
        self.success = success
        self.ip_address = ip_address

    def to_dict(self) -> Dict:
        base = super().to_dict()
        base.update(
            {
                "type": "login",
                "username": self.username,
                "success": self.success,
                "ip_address": self.ip_address,
            }
        )
        return base


class NetworkEvent(Event):
    """Represents a network traffic event.

    Captures network communication between two IP addresses including
    the amount of data transferred in both directions.
    """

    def __init__(
        self,
        src_ip: str,
        dst_ip: str,
        bytes_sent: int,
        bytes_received: int,
        source: str = "net_sensor",
        timestamp: Optional[datetime] = None,
    ) -> None:
        super().__init__(source, timestamp)
        self.src_ip = src_ip
        self.dst_ip = dst_ip
        self.bytes_sent = max(0, int(bytes_sent))
        self.bytes_received = max(0, int(bytes_received))

    def to_dict(self) -> Dict:
        base = super().to_dict()
        base.update(
            {
                "type": "network",
                "src_ip": self.src_ip,
                "dst_ip": self.dst_ip,
                "bytes_sent": self.bytes_sent,
                "bytes_received": self.bytes_received,
            }
        )
        return base


class SystemEvent(Event):
    """Represents a general system event.

    A flexible event type for capturing various system-level activities
    that don't fall into specific categories like login or network events.
    """

    def __init__(
        self,
        event_type: str,
        details: Dict,
        source: str = "system",
        timestamp: Optional[datetime] = None,
    ) -> None:
        super().__init__(source, timestamp)
        self.event_type = event_type
        self.details = details

    def to_dict(self) -> Dict:
        base = super().to_dict()
        base.update(
            {
                "type": "system",
                "event_type": self.event_type,
                "details": self.details,
            }
        )
        return base
