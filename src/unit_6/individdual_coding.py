"""
Thread-safe banking system with:
- BankAccount class
- Concurrent transaction simulation
- Deadlock-free transfers
- Unit tests for correctness and concurrency
"""

from __future__ import annotations

import threading
import random
import time
import unittest
from typing import Optional, List


# ============================================================
#  Custom exception
# ============================================================

class InsufficientFundsError(Exception):
    """Raised when withdrawing or transferring more than available balance."""
    pass


# ============================================================
#  Thread-safe, encapsulated BankAccount
# ============================================================

class BankAccount:
    """Thread-safe bank account (balance stored as integer cents)."""

    def __init__(self, account_number: str, initial_balance_cents: int = 0) -> None:
        if not account_number or not account_number.strip():
            raise ValueError("Account number must not be empty.")
        if initial_balance_cents < 0:
            raise ValueError("Initial balance cannot be negative.")

        self.__account_number: str = account_number
        self.__balance_cents: int = initial_balance_cents
        self.__lock = threading.RLock()

    # ------------ Public accessors ------------

    @property
    def account_number(self) -> str:
        """Read-only account number."""
        return self.__account_number

    def get_balance(self) -> int:
        """Return current balance in cents."""
        with self.__lock:
            return self.__balance_cents

    # ------------ Public operations ------------

    def deposit(self, amount_cents: int) -> None:
        """Deposit positive amount (in cents)."""
        if amount_cents <= 0:
            raise ValueError("Deposit amount must be positive.")
        with self.__lock:
            self.__deposit_unlocked(amount_cents)

    def withdraw(self, amount_cents: int) -> None:
        """Withdraw positive amount if funds are sufficient."""
        if amount_cents <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        with self.__lock:
            if amount_cents > self.__balance_cents:
                raise InsufficientFundsError("Insufficient funds.")
            self.__withdraw_unlocked(amount_cents)

    def transfer_to(self, other: "BankAccount", amount_cents: int) -> None:
        """
        Transfer from this account to another.
        Uses fixed lock ordering by account_number to avoid deadlocks.
        """
        if other is None:
            raise ValueError("Target account cannot be None.")
        if other is self:
            raise ValueError("Cannot transfer to the same account.")
        if amount_cents <= 0:
            raise ValueError("Transfer amount must be positive.")

        first, second = (
            self, other) if self.account_number < other.account_number else (other, self)

        with first.__lock:
            with second.__lock:
                if amount_cents > self.__balance_cents:
                    raise InsufficientFundsError(
                        "Insufficient funds for transfer.")
                self.__withdraw_unlocked(amount_cents)
                other.__deposit_unlocked(amount_cents)

    def __str__(self) -> str:
        return f"BankAccount({self.account_number}, balance_cents={self.get_balance()})"

    # ------------ Private helpers (internal only) ------------

    def __deposit_unlocked(self, amount_cents: int) -> None:
        self.__balance_cents += amount_cents

    def __withdraw_unlocked(self, amount_cents: int) -> None:
        self.__balance_cents -= amount_cents


# ============================================================
#  User task thread
# ============================================================

class UserTask(threading.Thread):
    """Simulated user performing random operations on one or two accounts."""

    def __init__(
        self,
        user_id: int,
        primary_account: BankAccount,
        secondary_account: Optional[BankAccount] = None,
        operations: int = 1000
    ) -> None:
        super().__init__(name=f"User-{user_id}")
        self.__primary_account = primary_account
        self.__secondary_account = secondary_account
        self.__operations = operations

    def run(self) -> None:
        for _ in range(self.__operations):
            action = random.choice(["deposit", "withdraw", "transfer"])
            # between £1.00 and £100.00
            amount_cents = random.randint(100, 10_000)

            try:
                if action == "deposit":
                    self.__primary_account.deposit(amount_cents)

                elif action == "withdraw":
                    try:
                        self.__primary_account.withdraw(amount_cents)
                    except InsufficientFundsError:
                        pass

                elif action == "transfer" and self.__secondary_account is not None:
                    # Random direction
                    if random.choice([True, False]):
                        try:
                            self.__primary_account.transfer_to(
                                self.__secondary_account, amount_cents)
                        except InsufficientFundsError:
                            pass
                    else:
                        try:
                            self.__secondary_account.transfer_to(
                                self.__primary_account, amount_cents)
                        except InsufficientFundsError:
                            pass

            except ValueError:
                # Defensive: should not occur given how amount is generated.
                pass

            time.sleep(0.0005)


# ============================================================
#  Transaction simulator
# ============================================================

class TransactionSimulator:
    """Creates accounts and user threads and runs a concurrent transaction simulation."""

    def __init__(
        self,
        initial_balance_a: int = 100_000,
        initial_balance_b: int = 100_000,
        user_count: int = 20,
        operations_per_user: int = 1_000
    ) -> None:
        self.__account_a = BankAccount("ACC-001", initial_balance_a)
        self.__account_b = BankAccount("ACC-002", initial_balance_b)
        self.__user_count = user_count
        self.__operations_per_user = operations_per_user
        self.__user_threads: List[UserTask] = []

    def total_balance(self) -> int:
        """Total balance across all accounts."""
        return self.__account_a.get_balance() + self.__account_b.get_balance()

    def run(self) -> None:
        """Run the transaction simulation."""
        print("=== Starting Simulation ===")
        print(f"Initial balance A: {self.__account_a.get_balance()}")
        print(f"Initial balance B: {self.__account_b.get_balance()}")
        print(f"Initial total:     {self.total_balance()}")
        print("===========================")

        self.__user_threads = [
            UserTask(i, self.__account_a, self.__account_b,
                     self.__operations_per_user)
            for i in range(self.__user_count)
        ]

        for t in self.__user_threads:
            t.start()

        for t in self.__user_threads:
            t.join()

        print("\n=== Simulation Finished ===")
        print(f"Final balance A: {self.__account_a.get_balance()}")
        print(f"Final balance B: {self.__account_b.get_balance()}")
        print(f"Final total:     {self.total_balance()}")
        print("===========================")

    # Optional read-only accessors if needed in tests/report
    @property
    def account_a(self) -> BankAccount:
        return self.__account_a

    @property
    def account_b(self) -> BankAccount:
        return self.__account_b


# ============================================================
#  Unit tests
# ============================================================

class TestBankAccountSingleThread(unittest.TestCase):
    """Single-threaded correctness tests."""

    def test_deposit_and_withdraw_single_thread(self) -> None:
        acc = BankAccount("TEST-001", 0)
        acc.deposit(10_000)   # £100
        acc.withdraw(4_000)   # £40
        self.assertEqual(6_000, acc.get_balance())

    def test_insufficient_funds_withdraw(self) -> None:
        acc = BankAccount("TEST-002", 2_000)
        with self.assertRaises(InsufficientFundsError):
            acc.withdraw(3_000)

    def test_invalid_amounts(self) -> None:
        acc = BankAccount("TEST-003", 1_000)
        with self.assertRaises(ValueError):
            acc.deposit(0)
        with self.assertRaises(ValueError):
            acc.withdraw(-100)
        with self.assertRaises(ValueError):
            acc.transfer_to(acc, 100)  # cannot transfer to self


class TestBankAccountConcurrency(unittest.TestCase):
    """Multi-threaded tests for thread safety and deadlocks."""

    def test_concurrent_deposit_and_withdraw(self) -> None:
        """Many threads deposit then withdraw same amount; final balance unchanged."""
        initial_balance = 50_000
        acc = BankAccount("CONC-001", initial_balance)

        def worker() -> None:
            for _ in range(1_000):
                acc.deposit(100)
                acc.withdraw(100)

        threads: List[threading.Thread] = []
        for _ in range(20):
            t = threading.Thread(target=worker)
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        self.assertEqual(initial_balance, acc.get_balance())

    def test_transfers_preserve_total_balance(self) -> None:
        """Total across two accounts unchanged by concurrent transfers."""
        acc_a = BankAccount("ACC-A", 100_000)
        acc_b = BankAccount("ACC-B", 200_000)
        initial_total = acc_a.get_balance() + acc_b.get_balance()

        def worker() -> None:
            for _ in range(1_000):
                try:
                    acc_a.transfer_to(acc_b, 50)
                    acc_b.transfer_to(acc_a, 50)
                except InsufficientFundsError:
                    pass

        threads: List[threading.Thread] = []
        for _ in range(30):
            t = threading.Thread(target=worker)
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        final_total = acc_a.get_balance() + acc_b.get_balance()
        self.assertEqual(initial_total, final_total)

    def test_deadlock_free_transfers(self) -> None:
        """Stress test: ensure transfer lock ordering avoids deadlock."""
        acc_a = BankAccount("AAA", 100_000)
        acc_b = BankAccount("BBB", 100_000)

        def worker() -> None:
            for _ in range(2_000):
                try:
                    acc_a.transfer_to(acc_b, 10)
                    acc_b.transfer_to(acc_a, 10)
                except InsufficientFundsError:
                    pass

        threads: List[threading.Thread] = []
        for _ in range(30):
            t = threading.Thread(target=worker)
            threads.append(t)
            t.start()

        for t in threads:
            t.join(timeout=10)

        all_finished = all(not t.is_alive() for t in threads)
        self.assertTrue(
            all_finished, "Possible deadlock: some threads did not finish.")


# ============================================================
#  Main entry point
# ============================================================

if __name__ == "__main__":
    simulator = TransactionSimulator(
        initial_balance_a=100_000,
        initial_balance_b=100_000,
        user_count=20,
        operations_per_user=1_000
    )
    simulator.run()

    print("\nRunning unit tests...\n")
    unittest.main(verbosity=2)
