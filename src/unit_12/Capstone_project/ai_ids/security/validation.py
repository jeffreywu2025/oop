from __future__ import annotations

import ipaddress
import re
from typing import Optional


USERNAME_RE = re.compile(r"^[A-Za-z0-9_.-]{1,64}$")


def validate_ip(ip: str) -> bool:
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False


def validate_username(username: str) -> bool:
    return bool(USERNAME_RE.fullmatch(username))


def safe_int(value: str, default: int = 0) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def sanitize_log_line(line: str, max_len: int = 512) -> str:
    # basic length cap to avoid abuse
    return line[:max_len]
