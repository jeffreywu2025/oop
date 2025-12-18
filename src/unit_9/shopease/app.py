"""ShopEase application factory module.

This module provides the build_app function which constructs and wires together
all the core application components including authentication, order processing,
and event publishing.
"""
from business.auth import AuthService
from business.events import EventBus, EmailNotifier
from business.order_service import OrderService
from presentation.controller import ShopController

# Repos would be real DB-backed classes; injected via interfaces.
# users_repo = ...
# products_repo = ...
# orders_repo = ...


def build_app(users_repo, products_repo, orders_repo) -> ShopController:
    """Build and configure the application with all dependencies.

    Constructs the complete application by instantiating and wiring together:
    - EventBus for asynchronous event publishing
    - AuthService for user authentication
    - OrderService for order processing
    - ShopController as the main entry point

    Args:
        users_repo: Repository implementing UserRepo protocol for user data access
        products_repo: Repository implementing ProductRepo protocol for product data access
        orders_repo: Repository implementing OrderRepo protocol for order data access

    Returns:
        ShopController: Configured controller instance ready for use
    """
    bus = EventBus()
    bus.subscribe(EmailNotifier())
    auth = AuthService(users_repo, pepper=b"SERVER_SECRET_PEPPER")
    orders = OrderService(products_repo, orders_repo, bus)
    return ShopController(auth, orders)
