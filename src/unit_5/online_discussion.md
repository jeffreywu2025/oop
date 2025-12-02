
The current implementation of PaymentProcessor exhibits several design issues. First, it violates the Open/Closed Principle, as introducing a new payment type requires modifying the existing class. This creates tight coupling, making the code more fragile and harder to test. Second, the expanding if–elif chain reduces readability and increases maintenance complexity, a common signal that behaviour should be delegated to specialised components instead of being embedded within a single method.

The Strategy Pattern resolves these issues by encapsulating each payment method in its own class implementing a shared interface. This allows PaymentProcessor to delegate behaviour to interchangeable strategies. Empirical evidence from Silva et al. (2021) demonstrates that applying the Strategy Pattern improves modularity and reduces overall code complexity in software systems. Likewise, Kulkarni and Bansal (2022) find that Strategy supports adherence to SOLID principles—particularly OCP—when managing multiple behavioural variations. Additionally, Dobrigkeit, Gonzalez-Huerta and Insfran (2023) show that design patterns such as Strategy contribute significantly to improved maintainability and reduced defect rates in industrial software projects.

Code:
```python
from abc import ABC, abstractmethod


class PaymentStrategy(ABC):
    @abstractmethod
    def pay(self, amount: float) -> None:
        pass


class CreditCardPayment(PaymentStrategy):
    def pay(self, amount):
        print(f"Processing credit card payment of ${amount}")


class PayPalPayment(PaymentStrategy):
    def pay(self, amount):
        print(f"Processing PayPal payment of ${amount}")


class BankTransferPayment(PaymentStrategy):
    def pay(self, amount):
        print(f"Processing bank transfer of ${amount}")


class PaymentProcessor:
    def __init__(self, strategy: PaymentStrategy):
        self.strategy = strategy

    def process_payment(self, amount):
        self.strategy.pay(amount)


# Usage
processor = PaymentProcessor(PayPalPayment())
processor.process_payment(100)
```

References:

Dobrigkeit, F., Gonzalez-Huerta, J. & Insfran, E. (2023) ‘Software design patterns and maintainability: An industrial empirical study’, Journal of Systems and Software, 197, 111608.

Kulkarni, A. & Bansal, A. (2022) ‘Strategy Design Pattern Applied on a Mobile App Building’, International Journal of Engineering Research & Technology, 11(1), pp. 1–6.

Silva, G., Costa, I. & Dias, L. (2021) ‘A Quasi-Experiment to Investigating the Impact of the Strategy Design Pattern’, Proceedings of the ACM SE Conference, pp. 1–6.
_____________________
Peer feedback to my post:

"
I concur with your analysis, particularly the assertion that the if-elif chain serves as a clear signal for delegating behaviour. What stood out to me in your post is the way you linked the strategy pattern directly to empirical evidence from recent studies. That strengthens the argument beyond theory. One aspect I’d add is how strategy improves modularity and makes runtime flexibility possible; for example, switching from PayPal to credit card processing without altering the core PaymentProcessor. Do you think this runtime adaptability is as important in real‑world payment systems as the maintainability benefits you highlighted"

_____________________
My reply:

"Hi Payman,

Thanks for your thoughtful response. I agree that runtime flexibility is a major additional benefit of the Strategy Pattern, especially for payment systems.

In real-world scenarios, being able to switch from PayPal to credit card (or to a backup provider) at runtime is very valuable. For example, if one gateway has an outage or higher fees for a specific region, the system can route payments through an alternative strategy without changing the PaymentProcessor code. This aligns with Silva et al. (2021), who found that Strategy-based designs support easier adaptation to change in evolving systems.

I would say runtime adaptability and maintainability are closely linked rather than competing concerns. The same decoupling that improves maintainability (Kulkarni & Bansal, 2022) also enables configuration-driven choice of strategy (e.g. via dependency injection, feature flags, or user preferences). Dobrigkeit et al. (2023) further emphasise that such pattern-driven modularity reduces the cost of introducing new variants.

That said, in payment domains there are also constraints: compliance, security, and auditing. So while we can swap strategies dynamically, in practice this tends to be controlled by configuration and policy rather than arbitrary runtime logic. Strategy gives us the technical capability; governance decides how far we use it.

So I’d conclude runtime adaptability is very important in payment systems, but it’s most powerful when combined with the maintainability and governance aspects we’ve both highlighted.

References

Dobrigkeit, F., Gonzalez-Huerta, J. & Insfran, E. (2023) Journal of Systems and Software, 197, 111608.


Kulkarni, A. & Bansal, A. (2022) International Journal of Engineering Research & Technology, 11(1), pp. 1–6.


Silva, G., Costa, I. & Dias, L. (2021) Proceedings of the ACM SE Conference, pp. 1–6."
