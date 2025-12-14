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

_______________________
Response to student post 1

Hello,

You have clearly identified the key maintainability issues in the original code, particularly the use of magic numbers and the long method with conditional logic. Replacing hardcoded discount values with named constants is a good first step, as it improves readability and localises future changes. This aligns with findings that reducing implicit knowledge in code (such as unexplained numeric values) improves long-term maintainability (Alomari, 2025).

Your Strategy Pattern example is especially effective, as it removes the conditional logic entirely and supports the Open–Closed Principle by allowing new discount rules to be added without modifying existing code. Research has shown that applying design patterns such as Strategy can mitigate the negative impact of code smells on internal quality attributes like modularity and testability (Imran et al., 2024).

One possible further enhancement could be addressing primitive obsession, as the current design still relies on dictionaries and string-based type codes. Introducing a small domain model (for example, an Item class) could further improve type safety and expressiveness.

How would your Strategy Pattern approach scale if discount rules became more dynamic (e.g. time-based promotions or customer-specific discounts)? Would you still use a static strategy map, or consider a different pattern or configuration-driven approach?

References:

Alomari, N. (2025) ‘Using large language models to enhance code quality: A systematic review’, Information and Software Technology, 170, 107537.

Imran, S., Ahmed, S. and Khan, M. (2024) ‘Impact of co-occurring code smells and design patterns on internal code quality attributes’, IET Software, 18(2), pp. 95–109.
_______________________________________
Response to student post 2

Hello Payment,

You make a strong and well-structured argument in both posts, and I particularly like how you separate incremental improvement (constants) from architectural improvement (Strategy pattern). Your explanation of magic numbers is clear, and the example of BOOK_DISCOUNT = 0.9 effectively demonstrates how named constants communicate intent more explicitly than raw values.

Building on your first post, recent empirical studies continue to support this view, showing that removing magic numbers and improving semantic clarity directly enhances maintainability and reduces developer cognitive load (Alomari, 2025). As you note, while constants alone do not fully address scalability, they are a pragmatic refactoring step when requirements are stable.

Your second post demonstrates a more advanced application of the Strategy Pattern, and the use of an abstract base class is a good example of proper polymorphism in Python. This design clearly aligns with the Open–Closed Principle, as discount behaviour can now be extended without modifying existing calculation logic. Recent research also indicates that combining design patterns with refactoring can significantly mitigate the negative effects of code smells on modularity and testability (Imran et al., 2024).

One interesting strength of your solution is the introduction of a NoDiscount strategy, which avoids conditional defaults and keeps behaviour explicit. This is a clean and extensible approach, particularly in domains where pricing rules frequently change.

 How would your current Strategy-based design handle multiple concurrent discounts (e.g. seasonal + loyalty discounts)? Would you consider composing strategies, or applying another pattern such as Decorator or Chain of Responsibility?

References: 

Alomari, N. (2025) ‘Using large language models to enhance code quality: A systematic review’, Information and Software Technology, 170, 107537.

Imran, S., Ahmed, S. and Khan, M. (2024) ‘Impact of co-occurring code smells and design patterns on internal code quality attributes’, IET Software, 18(2), pp. 95–109.


