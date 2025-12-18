"""Payment processing module.

Provides payment method implementations and factory for creating payment processors.
"""
from typing import Protocol
import secrets


class PaymentMethod(Protocol):
    """Protocol for payment processing implementations."""

    def charge(self, user_id: str, amount: int) -> str:
        """Process a payment charge.

        Args:
            user_id: ID of the user being charged
            amount: Amount to charge in cents

        Returns:
            str: Transaction ID for the payment
        """
        ...


class CardPayment:
    """Payment processor for credit/debit card transactions."""

    def charge(self, user_id: str, amount: int) -> str:
        """Process a card payment.

        Args:
            user_id: ID of the user being charged
            amount: Amount to charge in cents

        Returns:
            str: Generated transaction ID prefixed with 'txn_card_'
        """
        return "txn_card_" + secrets.token_hex(6)


class PayPalPayment:
    """Payment processor for PayPal transactions."""

    def charge(self, user_id: str, amount: int) -> str:
        """Process a PayPal payment.

        Args:
            user_id: ID of the user being charged
            amount: Amount to charge in cents

        Returns:
            str: Generated transaction ID prefixed with 'txn_pp_'
        """
        return "txn_pp_" + secrets.token_hex(6)


class PaymentFactory:
    """Factory for creating payment method instances."""

    methods = {"card": CardPayment, "paypal": PayPalPayment}

    @classmethod
    def create(cls, kind: str) -> PaymentMethod:
        """Create a payment method processor.

        Args:
            kind: Payment method identifier ("card" or "paypal")

        Returns:
            PaymentMethod: Configured payment processor instance

        Raises:
            KeyError: If payment method kind is not registered
        """
        return cls.methods[kind]()
