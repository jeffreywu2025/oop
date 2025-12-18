"""Unit tests for business services.

Tests authentication, order processing, and inventory management.
"""
import unittest
from typing import Dict, List

from business.auth import AuthService
from business.order_service import OrderService
from business.events import EventBus
from domain.models import User, Product, Order

# ---- In-memory repos (test doubles) ----


class MemUserRepo:
    """In-memory test double for UserRepo."""

    def __init__(self):
        """Initialize empty user storage."""
        self.by_email: Dict[str, User] = {}

    def get_by_email(self, email: str) -> User | None:
        """Retrieve user by email from memory."""
        return self.by_email.get(email)

    def add(self, user: User) -> None:
        """Store user in memory."""
        self.by_email[user.email] = user


class MemProductRepo:
    """In-memory test double for ProductRepo."""

    def __init__(self, products: List[Product]):
        """Initialize with a list of products."""
        self.p = {x.id: x for x in products}

    def get(self, pid: str) -> Product | None:
        """Retrieve product by ID from memory."""
        return self.p.get(pid)

    def search(self, q: str) -> List[Product]:
        """Search products by name from memory."""
        return [x for x in self.p.values() if q.lower() in x.name.lower()]

    def decrement_stock(self, pid: str, qty: int) -> None:
        """Reduce product stock, validating availability."""
        x = self.p[pid]
        if x.stock < qty:
            raise ValueError("out of stock")
        self.p[pid] = Product(x.id, x.name, x.price, x.stock - qty)


class MemOrderRepo:
    """In-memory test double for OrderRepo."""

    def __init__(self):
        """Initialize empty order storage."""
        self.orders: List[Order] = []

    def add(self, order: Order) -> None:
        """Store order in memory."""
        self.orders.append(order)

# ---- Tests ----


class TestAuth(unittest.TestCase):
    """Test cases for authentication service."""

    def test_register_and_login(self):
        """Test user registration and successful login."""
        users = MemUserRepo()
        auth = AuthService(users, pepper=b"pepper")
        auth.register("a@b.com", "pw123")
        self.assertTrue(auth.login("a@b.com", "pw123"))
        self.assertFalse(auth.login("a@b.com", "wrong"))


class TestOrder(unittest.TestCase):
    """Test cases for order service."""

    def test_place_order_decrements_stock_and_saves(self):
        """Test that orders decrement stock and are persisted."""
        products = MemProductRepo([Product("p1", "Mouse", 2000, 5)])
        orders = MemOrderRepo()
        bus = EventBus()
        svc = OrderService(products, orders, bus)

        o = svc.place_order("u1", {"p1": 2}, pay_kind="card")

        self.assertEqual(o.total, 4000)
        self.assertEqual(products.get("p1").stock, 3)
        self.assertEqual(len(orders.orders), 1)
        self.assertEqual(orders.orders[0].id, o.id)

    def test_out_of_stock_raises(self):
        """Test that orders fail when products are out of stock."""
        products = MemProductRepo([Product("p1", "Mouse", 2000, 1)])
        orders = MemOrderRepo()
        bus = EventBus()
        svc = OrderService(products, orders, bus)

        with self.assertRaises(AssertionError):
            svc.place_order("u1", {"p1": 2}, pay_kind="card")


if __name__ == "__main__":
    unittest.main()
