from user_management import EmailService


def test_email_service_prints_expected_output(capsys):
    # Arrange
    service = EmailService()

    # Act (real EmailService, no mocks)
    service.send_notification("jeff@example.com", "Welcome!")

    # Assert: verify observable behaviour
    captured = capsys.readouterr()
    assert "Sending email to jeff@example.com: Welcome!" in captured.out
