from __future__ import annotations
from abc import ABC, abstractmethod


# 1) Introduce an Interface (NotificationService)
class NotificationService(ABC):
    @abstractmethod
    def send_notification(self, user: str, message: str) -> None:
        """Send a notification to the user."""
        raise NotImplementedError


# 2) Implement the Interface (EmailService)
class EmailService(NotificationService):
    def send_notification(self, user: str, message: str) -> None:
        # In a real system this would call SMTP / an email provider API
        print(f"Sending email to {user}: {message}")


# Add More Services (SMSService)
class SMSService(NotificationService):
    def send_notification(self, user: str, message: str) -> None:
        print(f"Sending SMS to {user}: {message}")


# 3) Modify UserManager to Accept Dependency (DI)
class UserManager:
    """
    IoC: UserManager does NOT create its dependencies.
    DI: NotificationService is provided from outside (constructor injection).
    """

    def __init__(self, notifier: NotificationService) -> None:
        self.notifier = notifier

    def register_user(self, user: str) -> None:
        self.notifier.send_notification(user, "Welcome!")


# Composition root (manual IoC wiring) ---
def main() -> None:
    # Swap EmailService() -> SMSService() without changing UserManager
    notifier: NotificationService = EmailService()
    manager = UserManager(notifier)
    manager.register_user("jeff@example.com")


if __name__ == "__main__":
    main()
