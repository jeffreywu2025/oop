"""Order processing service module.

Handles order creation, payment processing, inventory management,
and order event publishing.
"""
import secrets
from typing import Dict
from data_access.interfaces import ProductRepo, OrderRepo
from domain.models import Order
from business.payments import PaymentFactory
from business.events import EventBus


class OrderService:
    """Service for managing order creation and processing.

    Coordinates inventory verification, payment processing, inventory updates,
    and order persistence with event publishing.
    """

    def __init__(self, products: ProductRepo, orders: OrderRepo, bus: EventBus):
        """Initialize the order service.

        Args:
            products: Repository implementing ProductRepo protocol
            orders: Repository implementing OrderRepo protocol
            bus: EventBus instance for publishing order events
        """
        self.products, self.orders, self.bus = products, orders, bus

    def place_order(self, user_id: str, items: Dict[str, int], pay_kind: str) -> Order:
        """Create and process an order with payment and inventory updates.

        Verifies product availability and stock levels, calculates total cost,
        processes payment, decrements stock for all items, creates the order record,
        and publishes an order_paid event.

        Args:
            user_id: ID of the user placing the order
            items: Dictionary mapping product IDs to quantities
            pay_kind: Payment method identifier (e.g., "card", "paypal")

        Returns:
            Order: Newly created order object with PAID status

        Raises:
            AssertionError: If product not found or insufficient stock
        """
        total = 0
        for pid, qty in items.items():
            p = self.products.get(pid)
            assert p and p.stock >= qty
            total += p.price * qty

        txn_id = PaymentFactory.create(pay_kind).charge(user_id, total)
        for pid, qty in items.items():
            self.products.decrement_stock(pid, qty)

        o = Order(secrets.token_hex(8), user_id, items, total, "PAID")
        self.orders.add(o)
        self.bus.publish("order_paid", {"order_id": o.id, "txn_id": txn_id})
        return o
