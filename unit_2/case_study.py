from abc import ABC, abstractmethod

# ============================================================
# TASK: Start with a poorly designed online shopping system
#       that violates several SOLID principles.
#
# PROBLEMS (as given in the prompt):
# - Single Responsibility Principle (SRP) violation:
#   The Order class handles cart management, total calculation,
#   and payment processing.
# - Open/Closed Principle (OCP) violation:
#   Adding a new payment method requires modifying Order.pay().
# - Dependency Inversion Principle (DIP) violation:
#   Order depends directly on concrete payment logic.
# ============================================================

# -----------------------------
# POOR / INITIAL DESIGN
# -----------------------------

class BadItem:
    """Simple product representation for the bad example."""

    def __init__(self, name: str, price: float):
        self.name = name
        self.price = price


class BadOrder:
    """Badly designed Order class (does too much)."""

    def __init__(self):
        self.items = []  # manages items

    def add_item(self, item: BadItem):
        self.items.append(item)

    def calculate_total(self) -> float:
        # calculates total
        return sum(item.price for item in self.items)

    def pay(self, payment_type: str):
        """
        Handles payment logic directly.

        - SRP: Violated (order + payment logic mixed).
        - OCP: Violated (each new payment type modifies this method).
        - DIP: Violated (depends on concrete payment logic).
        """
        if payment_type == "credit":
            print("Processing credit card payment...")
        elif payment_type == "paypal":
            print("Processing PayPal payment...")
        else:
            print("Unknown payment method.")


# ============================================================
# TASK: Refactor the system to follow SOLID principles.
#
# 1) Single Responsibility Principle (SRP)
#    - Order manages items and totals.
#    - Payment classes handle payments.
#
# 2) Open/Closed Principle (OCP)
#    - System is open for extension (new payment methods),
#      closed for modification (no need to change Order).
#
# 3) Liskov Substitution Principle (LSP)
#    - All PaymentMethod subclasses can replace the base class
#      without breaking behavior.
#
# 4) Interface Segregation Principle (ISP)
#    - Payment interface (PaymentMethod) is small and focused:
#      only pay(amount) is required.
#
# 5) Dependency Inversion Principle (DIP)
#    - High-level Order depends on an abstraction
#      (PaymentMethod), not concrete payment classes.
# ============================================================

# -----------------------------
# DOMAIN MODEL: PRODUCTS & ORDER
# -----------------------------

class Product:
    """Represents a product in the store."""

    def __init__(self, name: str, price: float):
        self.name = name
        self.price = price


class Order:
    """
    SRP: This class is responsible ONLY for managing items
    and calculating the total cost.
    """

    def __init__(self):
        self._items: list[Product] = []

    def add_item(self, product: Product) -> None:
        self._items.append(product)

    def calculate_total(self) -> float:
        return sum(item.price for item in self._items)

    def get_items(self) -> list[Product]:
        # could be used by UI / reporting
        return list(self._items)


# -----------------------------
# PAYMENT ABSTRACTION (ISP + DIP)
# -----------------------------

class PaymentMethod(ABC):
    """
    ISP: Interface is small and focused (only pay()).
    DIP: Order/clients depend on this abstraction.
    """

    @abstractmethod
    def pay(self, amount: float) -> None:
        """Process a payment of the given amount."""
        pass


# -----------------------------
# CONCRETE PAYMENT METHODS (OCP + LSP)
# -----------------------------

class CreditCardPayment(PaymentMethod):
    def __init__(self, card_number: str):
        self.card_number = card_number

    def pay(self, amount: float) -> None:
        # LSP: Can be used anywhere a PaymentMethod is expected.
        print(f"[CreditCard] Charging ${amount:.2f} to card {self.card_number}...")


class PayPalPayment(PaymentMethod):
    def __init__(self, email: str):
        self.email = email

    def pay(self, amount: float) -> None:
        print(f"[PayPal] Charging ${amount:.2f} to PayPal account {self.email}...")


class CryptoPayment(PaymentMethod):
    """Example of an easily added new payment method (OCP demo)."""

    def __init__(self, wallet_address: str):
        self.wallet_address = wallet_address

    def pay(self, amount: float) -> None:
        print(f"[Crypto] Sending crypto equivalent of ${amount:.2f} "
              f"from wallet {self.wallet_address}...")


# -----------------------------
# HIGH-LEVEL OPERATION USING DEPENDENCY INVERSION (DIP)
# -----------------------------

class CheckoutService:
    """
    High-level class that coordinates order checkout.
    DIP: Depends on PaymentMethod abstraction, not concrete classes.
    """

    @staticmethod
    def checkout(order: Order, payment_method: PaymentMethod) -> None:
        total = order.calculate_total()
        print(f"Order total: ${total:.2f}")
        payment_method.pay(total)
        print("Payment complete. Thank you for your purchase!\n")


# ============================================================
# SIMPLE DEMO / TEST
# (Not required by SOLID, just to show how it runs.)
# ============================================================

if __name__ == "__main__":
    # ----- Using the BAD design -----
    print("=== BAD DESIGN DEMO ===")
    bad_order = BadOrder()
    bad_order.add_item(BadItem("Keyboard", 50.0))
    bad_order.add_item(BadItem("Mouse", 25.0))
    print("Bad order total:", bad_order.calculate_total())
    bad_order.pay("credit")
    bad_order.pay("paypal")
    bad_order.pay("crypto")  # fails gracefully but requires code change to support

    # ----- Using the REFACTORED (SOLID) design -----
    print("\n=== SOLID DESIGN DEMO ===")

    order = Order()
    order.add_item(Product("Keyboard", 50.0))
    order.add_item(Product("Mouse", 25.0))
    order.add_item(Product("Monitor", 200.0))

    # Choose a payment method (any PaymentMethod subclass works)
    credit = CreditCardPayment(card_number="1234-5678-9012-3456")
    paypal = PayPalPayment(email="user@example.com")
    crypto = CryptoPayment(wallet_address="0xABCDEF123456")

    # Checkout using different payment methods without changing Order
    CheckoutService.checkout(order, credit)
    CheckoutService.checkout(order, paypal)
    CheckoutService.checkout(order, crypto)
