from unittest.mock import Mock
from user_management import UserManager, NotificationService


def test_register_user_sends_welcome_message_without_real_email():
    # Arrange: Mock NotificationService (no real email sending)
    mock_notifier: NotificationService = Mock(spec=NotificationService)
    manager = UserManager(mock_notifier)

    # Act
    manager.register_user("jeff@example.com")

    # Assert: UserManager logic is tested in isolation
    mock_notifier.send_notification.assert_called_once_with(
        "jeff@example.com", "Welcome!"
    )
