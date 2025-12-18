"""Controller module for request handling.

Provides the main entry point for the application's business logic.
"""
from typing import Dict
from business.auth import AuthService
from business.order_service import OrderService


class ShopController:
    """Main controller for shop operations.

    Coordinates authentication and order processing for customer checkout requests.
    """

    def __init__(self, auth: AuthService, orders: OrderService):
        """Initialize the shop controller.

        Args:
            auth: AuthService instance for user authentication
            orders: OrderService instance for order processing
        """
        self.auth, self.orders = auth, orders

    def checkout(self, email: str, pw: str, items: Dict[str, int], pay_kind: str):
        """Process a customer checkout request.

        Authenticates the user, verifies credentials, retrieves the user record,
        and creates an order with the specified items and payment method.

        Args:
            email: Customer's email address
            pw: Customer's password
            items: Dictionary mapping product IDs to quantities
            pay_kind: Payment method identifier

        Returns:
            Order: Newly created order object

        Raises:
            PermissionError: If email/password credentials are invalid
        """
        if not self.auth.login(email, pw):
            raise PermissionError("Invalid credentials")
        user = self.auth.users.get_by_email(email)
        return self.orders.place_order(user.id, items, pay_kind)
