from __future__ import annotations

import hashlib
import hmac
import time
from dataclasses import dataclass, field
from typing import Dict, Optional


@dataclass
class User:
    """Represents a user account in the authentication system.
    
    Stores user credentials in a secure format using password hashing
    and salt values. Tracks administrative privileges.
    """
    
    username: str
    password_hash: str
    salt: str
    is_admin: bool = False


@dataclass
class AuthState:
    """Maintains the state of the authentication system.
    
    Tracks registered users, failed login attempts, and timing information
    for implementing account lockout and brute force protection.
    """
    
    users: Dict[str, User] = field(default_factory=dict)
    failed_attempts: Dict[str, int] = field(default_factory=dict)
    last_attempt_ts: Dict[str, float] = field(default_factory=dict)

    max_attempts: int = 5
    lockout_window_sec: int = 60


class AuthService:
    """
    Very simple in-memory auth system.
    
    """

    def __init__(self, state: Optional[AuthState] = None) -> None:
        self.state = state or AuthState()

    def _hash_password(self, password: str, salt: str) -> str:
        # PBKDF2 would be better; using SHA256 here just as a placeholder.
        return hashlib.sha256((salt + password).encode("utf-8")).hexdigest()

    def register(self, username: str, password: str, is_admin: bool = False) -> None:
        if username in self.state.users:
            raise ValueError("User already exists")
        salt = hashlib.sha256(username.encode("utf-8")).hexdigest()[:16]
        password_hash = self._hash_password(password, salt)
        self.state.users[username] = User(
            username=username,
            password_hash=password_hash,
            salt=salt,
            is_admin=is_admin,
        )

    def verify(self, username: str, password: str) -> bool:
        now = time.time()
        attempts = self.state.failed_attempts.get(username, 0)
        last_ts = self.state.last_attempt_ts.get(username, 0.0)

        if attempts >= self.state.max_attempts and (now - last_ts) < self.state.lockout_window_sec:
            return False

        user = self.state.users.get(username)
        if not user:
            return False

        candidate_hash = self._hash_password(password, user.salt)
        ok = hmac.compare_digest(candidate_hash, user.password_hash)

        self.state.last_attempt_ts[username] = now
        if ok:
            self.state.failed_attempts[username] = 0
        else:
            self.state.failed_attempts[username] = attempts + 1
        return ok
