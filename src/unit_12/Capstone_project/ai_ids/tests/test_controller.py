from __future__ import annotations

from controller.config import DetectionContext, SecurityConfig
from controller.core import IDSController
from detectors.rules import EventFloodRule
from detectors.rules import RuleBasedDetector
from events.base import LoginEvent


class DummyAction:
    """Test helper class for verifying action execution.
    
    A simple mock action that records whether it has been called,
    used for testing the IDS controller's action triggering behavior.
    """
    
    def __init__(self) -> None:
        self.called = False

    def execute(self, result, event, ctx) -> None:
        self.called = True


def test_ids_controller_triggers_action_on_rule_match():
    config = SecurityConfig(event_flood_threshold=1, event_flood_window_sec=10)
    ids = IDSController(config=config)

    rule = EventFloodRule(max_events=1, window_sec=10)
    detector = RuleBasedDetector([rule])
    ids.add_detector(detector)

    action = DummyAction()
    ids.add_action(action)

    event = LoginEvent(username="alice", success=False, ip_address="203.0.113.5")
    ids.consume(event)
    # Second event should trigger the flood rule
    ids.consume(event)

    assert action.called is True
