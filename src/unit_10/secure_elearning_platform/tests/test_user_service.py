import unittest

from elearn.user_management import (
    AlreadyExistsError,
    AuthenticationError,
    InMemoryUserRepository,
    NotFoundError,
    PasswordHasher,
    UserService,
    ValidationError,
)

class UserServiceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.repo = InMemoryUserRepository()
        # Use lower (but still >= 10_000) iterations to keep tests fast.
        self.hasher = PasswordHasher(iterations=10_000, salt_bytes=16, dklen=32)
        self.svc = UserService(self.repo, self.hasher)

    def test_register_user_success(self):
        user = self.svc.register_user("Alice@example.com", "correct horse battery staple", "Alice A.")
        self.assertEqual(user.email, "alice@example.com")
        self.assertTrue(user.is_active)
        self.assertIn("student", user.roles)
        # Stored hash should not contain plaintext.
        self.assertNotIn("correct horse", user.password_hash)

    def test_register_user_duplicate_email_raises(self):
        self.svc.register_user("bob@example.com", "long-enough-password", "Bob B.")
        with self.assertRaises(AlreadyExistsError):
            self.svc.register_user("BOB@EXAMPLE.COM", "another-long-enough-password", "Bob B.2")

    def test_register_user_invalid_email_raises(self):
        with self.assertRaises(ValidationError):
            self.svc.register_user("not-an-email", "long-enough-password", "Name")

    def test_register_user_short_password_raises(self):
        with self.assertRaises(ValidationError):
            self.svc.register_user("c@example.com", "short", "C")

    def test_authenticate_success(self):
        self.svc.register_user("d@example.com", "long-enough-password", "D")
        user = self.svc.authenticate("d@example.com", "long-enough-password")
        self.assertEqual(user.email, "d@example.com")

    def test_authenticate_wrong_password_raises(self):
        self.svc.register_user("e@example.com", "long-enough-password", "E")
        with self.assertRaises(AuthenticationError):
            self.svc.authenticate("e@example.com", "wrong-password")

    def test_authenticate_nonexistent_user_raises(self):
        with self.assertRaises(AuthenticationError):
            self.svc.authenticate("missing@example.com", "any-password")

    def test_change_password_success(self):
        user = self.svc.register_user("f@example.com", "old-password-1234", "F")
        self.svc.change_password(user.user_id, "old-password-1234", "new-password-1234")
        # old password no longer works
        with self.assertRaises(AuthenticationError):
            self.svc.authenticate("f@example.com", "old-password-1234")
        # new password works
        self.svc.authenticate("f@example.com", "new-password-1234")

    def test_change_password_wrong_old_password_raises(self):
        user = self.svc.register_user("g@example.com", "old-password-1234", "G")
        with self.assertRaises(AuthenticationError):
            self.svc.change_password(user.user_id, "WRONG", "new-password-1234")

    def test_change_password_user_not_found_raises(self):
        with self.assertRaises(NotFoundError):
            self.svc.change_password("no-such-id", "old", "new-password-1234")

    def test_disable_user_prevents_authentication(self):
        user = self.svc.register_user("h@example.com", "long-enough-password", "H")
        self.svc.disable_user(user.user_id)
        with self.assertRaises(AuthenticationError):
            self.svc.authenticate("h@example.com", "long-enough-password")

    def test_assign_and_remove_role(self):
        user = self.svc.register_user("i@example.com", "long-enough-password", "I")
        self.svc.assign_role(user.user_id, "instructor")
        updated = self.svc.get_user(user.user_id)
        self.assertIn("instructor", updated.roles)

        self.svc.remove_role(user.user_id, "instructor")
        updated2 = self.svc.get_user(user.user_id)
        self.assertNotIn("instructor", updated2.roles)

    def test_assign_unknown_role_raises(self):
        user = self.svc.register_user("j@example.com", "long-enough-password", "J")
        with self.assertRaises(ValidationError):
            self.svc.assign_role(user.user_id, "superuser")

    def test_list_users_returns_all(self):
        self.svc.register_user("k1@example.com", "long-enough-password", "K1")
        self.svc.register_user("k2@example.com", "long-enough-password", "K2")
        users = self.svc.list_users()
        self.assertEqual(len(users), 2)

if __name__ == "__main__":
    unittest.main()
