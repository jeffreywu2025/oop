"""Authentication service module.

Handles user registration and login with secure password hashing using PBKDF2.
"""
import hashlib
import hmac
import secrets
from data_access.interfaces import UserRepo
from domain.models import User


class AuthService:
    """Service for managing user authentication and registration.

    Provides secure password hashing with salt and pepper, user registration,
    and login verification using constant-time comparison.
    """

    def __init__(self, users: UserRepo, pepper: bytes):
        """Initialize the authentication service.

        Args:
            users: Repository implementing UserRepo protocol for persistent storage
            pepper: Server-side secret bytes used in password hashing
        """
        self.users, self.pepper = users, pepper

    def _hash(self, pw: str, salt: bytes) -> str:
        """Hash a password using PBKDF2-HMAC-SHA256.

        Combines the provided salt with the server pepper to create a
        secure hash resistant to rainbow table attacks.

        Args:
            pw: Plain text password to hash
            salt: Random bytes unique to this password

        Returns:
            str: Hexadecimal representation of the hash
        """
        return hashlib.pbkdf2_hmac("sha256", pw.encode(), salt + self.pepper, 200_000).hex()

    def register(self, email: str, pw: str) -> User:
        """Register a new user with email and password.

        Generates a unique user ID, creates a random salt, hashes the password,
        and persists the user record.

        Args:
            email: User's email address
            pw: User's plain text password

        Returns:
            User: Newly created and registered user object
        """
        salt = secrets.token_bytes(16)
        u = User(secrets.token_hex(8), email,
                 salt.hex() + ":" + self._hash(pw, salt))
        self.users.add(u)
        return u

    def login(self, email: str, pw: str) -> bool:
        """Verify user credentials via email and password.

        Retrieves the user record, extracts the salt, recomputes the hash,
        and compares using constant-time comparison to prevent timing attacks.

        Args:
            email: User's email address
            pw: User's plain text password

        Returns:
            bool: True if credentials are valid, False otherwise
        """
        u = self.users.get_by_email(email)
        if not u:
            return False
        salt_hex, stored = u.pw_hash.split(":")
        check = self._hash(pw, bytes.fromhex(salt_hex))
        return hmac.compare_digest(stored, check)
