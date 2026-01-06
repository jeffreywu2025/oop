from __future__ import annotations

import logging
import time

from actions.actions import AlertAction, BlockIPAction, LogAction, EmailAlertAction
from controller.config import SecurityConfig
from controller.core import IDSController
from controller.event_bus import EventBus
from datasource.log_file_source import LogFileDataSource
from datasource.simulated_source import SimulatedDataSource
from detectors.ml import MLAnomalyDetector
from detectors.rules import (
    EventFloodRule,
    FailedLoginBurstRule,
    RuleBasedDetector,
    SuspiciousIPRule,
)
from security.auth import AuthService
from security.validation import validate_username

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
)
logger = logging.getLogger("IDS.main")


def build_ids() -> tuple[EventBus, IDSController, SimulatedDataSource]:
    config = SecurityConfig(
        blacklisted_ips={"198.51.100.10"},
        event_flood_threshold=50,
        event_flood_window_sec=5,
        anomaly_threshold=0.9,
    )

    ids = IDSController(config=config)

    rules = [
        FailedLoginBurstRule(threshold=3, window_sec=10),
        SuspiciousIPRule(blacklist=config.blacklisted_ips),
        EventFloodRule(
            max_events=config.event_flood_threshold,
            window_sec=config.event_flood_window_sec,
        ),
    ]
    rule_detector = RuleBasedDetector(rules)
    # Use real scikit-learn based ML detector with lower threshold for more sensitive detection
    ml_detector = MLAnomalyDetector(threshold=0.6)

    ids.add_detector(rule_detector)
    ids.add_detector(ml_detector)

    # Existing actions
    ids.add_action(AlertAction())
    ids.add_action(BlockIPAction())
    ids.add_action(LogAction())
    # New email alert action
    ids.add_action(EmailAlertAction(recipient="security@example.com"))

    bus = EventBus()
    bus.subscribe(ids)

    sim = SimulatedDataSource(event_bus=bus, interval_sec=0.3)
    return bus, ids, sim


def cli_login(auth: AuthService) -> bool:
    print("=== IDS Admin Login ===")
    username = input("Username: ").strip()
    password = input("Password: ").strip()

    if not validate_username(username):
        print("Invalid username format.")
        return False

    if not auth.verify(username, password):
        print("Login failed.")
        return False

    user = auth.state.users.get(username)
    if not user or not user.is_admin:
        print("Access denied: admin privileges required.")
        return False

    print(f"Welcome, {username}.")
    return True


def main() -> None:
    auth = AuthService()
    # Register a default admin user for demo purposes
    # In a real system, this would be pre-provisioned and not hard-coded.
    auth.register("admin", "admin123", is_admin=True)

    if not cli_login(auth):
        print("Exiting.")
        return

    bus, ids, sim = build_ids()

    while True:
        print("\n=== IDS CLI ===")
        print("1. Run simulated demo")
        print("2. Replay from log file")
        print("3. Exit")
        choice = input("Select option: ").strip()

        if choice == "1":
            bus.start()
            sim.start()
            try:
                print("Running simulated IDS for 10 seconds...")
                time.sleep(10)
            finally:
                sim.stop()
                bus.stop()
        elif choice == "2":
            path = input("Enter log file path: ").strip()
            bus.start()
            source = LogFileDataSource(event_bus=bus, file_path=path)
            source.replay()
            time.sleep(2)
            bus.stop()
        elif choice == "3":
            print("Goodbye.")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
