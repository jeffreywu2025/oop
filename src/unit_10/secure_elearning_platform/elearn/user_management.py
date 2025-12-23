"""
User Management module for a secure e-learning platform.

This module is intentionally framework-agnostic. It provides:
- Domain model: User, Role
- Repository abstractions: UserRepository (Protocol) and InMemoryUserRepository
- Security primitives: PasswordHasher (PBKDF2-HMAC-SHA256) and TokenService
- Service layer: UserService (registration, authentication, password change, role management)

Design notes
------------
* Password hashing: PBKDF2-HMAC-SHA256 with per-user random salt.
  The iteration count is configurable to support fast unit tests and
  stronger production settings.
* Constant-time comparisons: hmac.compare_digest.
* Input validation: email format, password length, role whitelist.

This module is suitable for a layered architecture:
- Domain (entities/exceptions)
- Services (business logic)
- Infrastructure (repository implementations)

"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict, Iterable, Optional, Protocol, Set
import base64
import hashlib
import hmac
import re
import secrets
import uuid


# ----------------------------
# Exceptions (public API)
# ----------------------------

class UserError(Exception):
    """Base exception for user-management errors."""


class ValidationError(UserError):
    """Raised when input validation fails."""


class AlreadyExistsError(UserError):
    """Raised when a unique constraint is violated (e.g., email already registered)."""


class NotFoundError(UserError):
    """Raised when an entity cannot be found."""


class AuthenticationError(UserError):
    """Raised when authentication fails."""


# ----------------------------
# Domain model
# ----------------------------

_EMAIL_RE = re.compile(r"^[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}$")


@dataclass(frozen=True)
class Role:
    """Represents an authorization role."""
    name: str


@dataclass
class User:
    """
    Represents a platform user.

    Attributes:
        user_id: Stable UUID for the user.
        email: Unique email address (case-insensitive uniqueness recommended).
        full_name: Display name.
        password_hash: Encoded password hash string.
        roles: Set of role names.
        is_active: Whether the account is active.
        created_at: UTC creation timestamp.
        updated_at: UTC last update timestamp.
    """
    user_id: str
    email: str
    full_name: str
    password_hash: str
    roles: Set[str] = field(default_factory=set)
    is_active: bool = True
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def touch(self) -> None:
        """Update the updated_at timestamp."""
        self.updated_at = datetime.now(timezone.utc)


# ----------------------------
# Repositories
# ----------------------------

class UserRepository(Protocol):
    """Persistence interface for users."""

    def add(self, user: User) -> None:
        """Persist a new user."""
        ...

    def get_by_email(self, email: str) -> Optional[User]:
        """Return a user by email or None if not found."""
        ...

    def get_by_id(self, user_id: str) -> Optional[User]:
        """Return a user by ID or None if not found."""
        ...

    def update(self, user: User) -> None:
        """Persist changes to an existing user."""
        ...

    def list_all(self) -> Iterable[User]:
        """Return all users."""
        ...


class InMemoryUserRepository:
    """
    In-memory repository (for unit tests / prototypes).

    NOTE: Not safe for production because it does not persist and does not
    provide concurrency guarantees.
    """

    def __init__(self) -> None:
        self._by_id: Dict[str, User] = {}
        self._by_email_lower: Dict[str, str] = {}  # email_lower -> user_id

    def add(self, user: User) -> None:
        email_key = user.email.strip().lower()
        if email_key in self._by_email_lower:
            raise AlreadyExistsError("Email already registered.")
        self._by_id[user.user_id] = user
        self._by_email_lower[email_key] = user.user_id

    def get_by_email(self, email: str) -> Optional[User]:
        email_key = (email or "").strip().lower()
        user_id = self._by_email_lower.get(email_key)
        return self._by_id.get(user_id) if user_id else None

    def get_by_id(self, user_id: str) -> Optional[User]:
        return self._by_id.get(user_id)

    def update(self, user: User) -> None:
        if user.user_id not in self._by_id:
            raise NotFoundError("User not found.")
        self._by_id[user.user_id] = user
        self._by_email_lower[user.email.strip().lower()] = user.user_id

    def list_all(self) -> Iterable[User]:
        return list(self._by_id.values())


# ----------------------------
# Security primitives
# ----------------------------

class PasswordHasher:
    """
    Password hashing utility using PBKDF2-HMAC-SHA256.

    Encoded format:
        pbkdf2_sha256$<iterations>$<salt_b64>$<dk_b64>

    Args:
        iterations: PBKDF2 iteration count.
        salt_bytes: Salt length in bytes.
        dklen: Derived key length in bytes.

    Security:
        * Uses per-user random salt (secrets.token_bytes).
        * Uses constant-time compare on verification.
    """

    def __init__(self, *, iterations: int = 200_000, salt_bytes: int = 16, dklen: int = 32) -> None:
        if iterations < 10_000:
            raise ValueError("iterations too low for realistic security; use >= 10_000")
        if salt_bytes < 16:
            raise ValueError("salt_bytes should be >= 16")
        if dklen < 32:
            raise ValueError("dklen should be >= 32")
        self.iterations = iterations
        self.salt_bytes = salt_bytes
        self.dklen = dklen

    def hash_password(self, password: str) -> str:
        """Hash a password and return encoded hash string."""
        if not isinstance(password, str):
            raise ValidationError("Password must be a string.")
        salt = secrets.token_bytes(self.salt_bytes)
        dk = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt,
            self.iterations,
            dklen=self.dklen,
        )
        return self._encode(self.iterations, salt, dk)

    def verify_password(self, password: str, encoded_hash: str) -> bool:
        """Verify a password against an encoded hash string."""
        try:
            algo, it_s, salt_b64, dk_b64 = encoded_hash.split("$", 3)
            if algo != "pbkdf2_sha256":
                return False
            iterations = int(it_s)
            salt = base64.urlsafe_b64decode(self._pad_b64(salt_b64).encode("ascii"))
            expected = base64.urlsafe_b64decode(self._pad_b64(dk_b64).encode("ascii"))
        except Exception:
            return False

        candidate = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt,
            iterations,
            dklen=len(expected),
        )
        return hmac.compare_digest(candidate, expected)
    @staticmethod
    def _pad_b64(s: str) -> str:
        """Pad a URL-safe Base64 string (without '=') to valid length."""
        return s + "=" * ((4 - (len(s) % 4)) % 4)



    @staticmethod
    def _encode(iterations: int, salt: bytes, dk: bytes) -> str:
        salt_b64 = base64.urlsafe_b64encode(salt).decode("ascii").rstrip("=")
        dk_b64 = base64.urlsafe_b64encode(dk).decode("ascii").rstrip("=")
        return f"pbkdf2_sha256${iterations}${salt_b64}${dk_b64}"


class TokenService:
    """Generates cryptographically strong, URL-safe tokens (e.g., for password reset)."""

    @staticmethod
    def generate_token(nbytes: int = 32) -> str:
        """
        Generate a URL-safe token.

        Args:
            nbytes: Random bytes before Base64 encoding.
        """
        if nbytes < 16:
            raise ValueError("nbytes must be >= 16")
        return secrets.token_urlsafe(nbytes)


# ----------------------------
# Service layer
# ----------------------------

class UserService:
    """
    High-level use cases for user management.

    Public methods are intended to be unit-tested.

    Args:
        repo: A UserRepository implementation.
        hasher: PasswordHasher.
        allowed_roles: Optional whitelist of allowed role names.
    """

    def __init__(self, repo: UserRepository, hasher: PasswordHasher, *, allowed_roles: Optional[Set[str]] = None) -> None:
        self._repo = repo
        self._hasher = hasher
        self._allowed_roles = allowed_roles or {"student", "instructor", "admin"}

    # ---- Public API ----

    def register_user(self, email: str, password: str, full_name: str, *, roles: Optional[Set[str]] = None) -> User:
        """
        Register a new user.

        Raises:
            ValidationError, AlreadyExistsError
        """
        email_n = self._validate_email(email)
        name_n = self._validate_full_name(full_name)
        self._validate_password(password)
        roles_n = self._validate_roles(roles or {"student"})

        if self._repo.get_by_email(email_n) is not None:
            raise AlreadyExistsError("Email already registered.")

        user = User(
            user_id=str(uuid.uuid4()),
            email=email_n,
            full_name=name_n,
            password_hash=self._hasher.hash_password(password),
            roles=set(roles_n),
            is_active=True,
        )
        self._repo.add(user)
        return user

    def authenticate(self, email: str, password: str) -> User:
        """
        Authenticate a user by email and password.

        Returns:
            The authenticated User.

        Raises:
            AuthenticationError
        """
        email_n = (email or "").strip().lower()
        user = self._repo.get_by_email(email_n)
        # Avoid revealing whether the email exists.
        if user is None or not user.is_active:
            raise AuthenticationError("Invalid credentials.")

        if not self._hasher.verify_password(password, user.password_hash):
            raise AuthenticationError("Invalid credentials.")
        return user

    def change_password(self, user_id: str, old_password: str, new_password: str) -> None:
        """
        Change password for a user.

        Raises:
            NotFoundError, AuthenticationError, ValidationError
        """
        user = self._repo.get_by_id(user_id)
        if user is None:
            raise NotFoundError("User not found.")
        if not user.is_active:
            raise AuthenticationError("Account disabled.")

        if not self._hasher.verify_password(old_password, user.password_hash):
            raise AuthenticationError("Invalid credentials.")

        self._validate_password(new_password)
        user.password_hash = self._hasher.hash_password(new_password)
        user.touch()
        self._repo.update(user)

    def disable_user(self, user_id: str) -> None:
        """Disable (deactivate) a user account."""
        user = self._repo.get_by_id(user_id)
        if user is None:
            raise NotFoundError("User not found.")
        user.is_active = False
        user.touch()
        self._repo.update(user)

    def assign_role(self, user_id: str, role: str) -> None:
        """
        Assign a role to a user.

        Raises:
            NotFoundError, ValidationError
        """
        user = self._repo.get_by_id(user_id)
        if user is None:
            raise NotFoundError("User not found.")
        role_n = self._validate_roles({role}).pop()
        user.roles.add(role_n)
        user.touch()
        self._repo.update(user)

    def remove_role(self, user_id: str, role: str) -> None:
        """
        Remove a role from a user.

        Raises:
            NotFoundError, ValidationError
        """
        user = self._repo.get_by_id(user_id)
        if user is None:
            raise NotFoundError("User not found.")
        role_n = self._validate_roles({role}).pop()
        user.roles.discard(role_n)
        user.touch()
        self._repo.update(user)

    def get_user(self, user_id: str) -> User:
        """Get a user by ID."""
        user = self._repo.get_by_id(user_id)
        if user is None:
            raise NotFoundError("User not found.")
        return user

    def list_users(self) -> list[User]:
        """List all users."""
        return list(self._repo.list_all())

    # ---- Validation helpers ----

    def _validate_email(self, email: str) -> str:
        email_n = (email or "").strip().lower()
        if not email_n or len(email_n) > 254 or not _EMAIL_RE.match(email_n):
            raise ValidationError("Invalid email address.")
        return email_n

    def _validate_full_name(self, full_name: str) -> str:
        name_n = (full_name or "").strip()
        if not name_n or len(name_n) > 100:
            raise ValidationError("Invalid full name.")
        return name_n

    def _validate_password(self, password: str) -> None:
        # Simple baseline policy; can be replaced with a stronger policy / zxcvbn, etc.
        if not isinstance(password, str):
            raise ValidationError("Password must be a string.")
        if len(password) < 12:
            raise ValidationError("Password too short (min 12 characters).")
        if len(password) > 128:
            raise ValidationError("Password too long (max 128 characters).")

    def _validate_roles(self, roles: Set[str]) -> Set[str]:
        cleaned = {r.strip().lower() for r in roles if (r or "").strip()}
        if not cleaned:
            raise ValidationError("At least one role is required.")
        unknown = cleaned - self._allowed_roles
        if unknown:
            raise ValidationError(f"Unknown role(s): {', '.join(sorted(unknown))}")
        return cleaned
