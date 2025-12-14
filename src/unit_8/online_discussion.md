Unit 8 Collaborative Discussion

The given pricing function is functional but exhibits several design issues that negatively impact maintainability and readability.
The first clear code smell is the use of magic numbers. Discount factors (0.9, 0.8) are embedded directly in the logic, obscuring business intent and tightly coupling pricing rules to the calculation method. Such hardcoding reduces readability and increases maintenance effort when discount policies change (Alomari, 2025).

The second issue is conditional complexity caused by type codes. Behaviour is selected using string comparisons on item["type"], concentrating multiple pricing rules within a single method. As new item types are introduced, this function must be modified, violating the Open–Closed Principle and increasing the likelihood of defects (Imran et al., 2024).

A related design concern is primitive obsession. Representing items as dictionaries with string keys instead of domain objects weakens type safety and reduces expressiveness, making the code more error-prone and harder to evolve.
Option 1 – Data-driven refactoring (simpler systems)

```python
DISCOUNTS = {"book": 0.9, "electronics": 0.8}

def calculate_total_price(items):
    return sum(i["price"] * DISCOUNTS.get(i["type"], 1.0) for i in items)
```

This approach removes magic numbers and centralises discount configuration, improving readability and ease of change.

Option 2 – Strategy Pattern (scalable design)
```python
class Discount:
    def apply(self, price): return price

class BookDiscount(Discount):
    def apply(self, price): return price * 0.9

class ElectronicsDiscount(Discount):
    def apply(self, price): return price * 0.8
```

Encapsulating discount logic within strategy classes eliminates conditional complexity and enables new pricing rules to be added without modifying existing code. This design aligns with SOLID principles and has been shown to mitigate the negative impact of code smells on internal code quality (Imran et al., 2024).

References:

Alomari, N. (2025) ‘Using large language models to enhance code quality: A systematic review’, Information and Software Technology, 170, 107537.
Imran, S., Ahmed, S. and Khan, M. (2024) ‘Impact of co-occurring code smells and design patterns on internal code quality attributes’, IET Software, 18(2), pp. 95–109.
