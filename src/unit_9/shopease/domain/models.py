"""Domain models module.

Defines the core data models for users, products, and orders.
"""
from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class User:
    """Represents a user account.

    Attributes:
        id: Unique user identifier
        email: User's email address
        pw_hash: Salted and hashed password (format: salt:hash)
    """
    id: str
    email: str
    pw_hash: str


@dataclass(frozen=True)
class Product:
    """Represents a product in the catalog.

    Attributes:
        id: Unique product identifier
        name: Product name
        price: Price in cents
        stock: Available quantity in inventory
    """
    id: str
    name: str
    price: int
    stock: int


@dataclass(frozen=True)
class Order:
    """Represents a customer order.

    Attributes:
        id: Unique order identifier
        user_id: ID of the user who placed the order
        items: Dictionary mapping product IDs to quantities ordered
        total: Total order amount in cents
        status: Order status (e.g., "PAID", "SHIPPED")
    """
    id: str
    user_id: str
    items: Dict[str, int]
    total: int
    status: str
