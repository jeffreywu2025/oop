"""Event bus and notification module.

Implements the observer pattern for asynchronous event publishing and handling.
"""
from typing import Protocol, List


class Observer(Protocol):
    """Protocol for event observers."""

    def notify(self, event: str, payload: dict) -> None:
        """Handle a published event.

        Args:
            event: Event type identifier
            payload: Event data as dictionary
        """
        ...


class EmailNotifier:
    """Observer that handles email notifications for events."""

    def notify(self, event: str, payload: dict) -> None:
        """Process an event and send email notification if applicable.

        Args:
            event: Event type identifier
            payload: Event data containing notification details
        """
        pass


class EventBus:
    """Simple event bus for publishing events to multiple subscribers.

    Implements the observer pattern to decouple event producers from consumers.
    """

    def __init__(self):
        """Initialize the event bus with an empty subscriber list."""
        self._subs: List[Observer] = []

    def subscribe(self, obs: Observer) -> None:
        """Register an observer to receive published events.

        Args:
            obs: Observer instance implementing the Observer protocol
        """
        self._subs.append(obs)

    def publish(self, event: str, payload: dict) -> None:
        """Publish an event to all subscribed observers.

        Args:
            event: Event type identifier
            payload: Event data to deliver to observers
        """
        for s in self._subs:
            s.notify(event, payload)
