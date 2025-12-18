"""Data access layer interfaces module.

Defines repository protocols for database abstraction.
"""
from typing import Protocol, Dict, List
from domain.models import User, Product, Order


class UserRepo(Protocol):
    """Repository interface for user data access.

    Defines the contract for persisting and retrieving user records.
    """

    def get_by_email(self, email: str) -> User | None:
        """Retrieve a user by email address.

        Args:
            email: User's email address

        Returns:
            User object if found, None otherwise
        """
        ...

    def add(self, user: User) -> None:
        """Persist a new user record.

        Args:
            user: User object to store
        """
        ...


class ProductRepo(Protocol):
    """Repository interface for product data access.

    Defines the contract for retrieving and modifying product records.
    """

    def get(self, pid: str) -> Product | None:
        """Retrieve a product by ID.

        Args:
            pid: Product identifier

        Returns:
            Product object if found, None otherwise
        """
        ...

    def search(self, q: str) -> List[Product]:
        """Search for products by name or description.

        Args:
            q: Search query string

        Returns:
            List of Product objects matching the query
        """
        ...

    def decrement_stock(self, pid: str, qty: int) -> None:
        """Reduce product stock by the specified quantity.

        Args:
            pid: Product identifier
            qty: Quantity to decrement

        Raises:
            ValueError: If attempting to decrement below zero
        """
        ...


class OrderRepo(Protocol):
    """Repository interface for order data access.

    Defines the contract for persisting order records.
    """

    def add(self, order: Order) -> None:
        """Persist a new order record.

        Args:
            order: Order object to store
        """
        ...
