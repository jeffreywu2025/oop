Unit 11 coding exercise

1. Purpose of the Task

The purpose of this task was to refactor a simple Python application to apply Dependency Injection (DI) and Inversion of Control (IoC) principles in order to improve software maintainability, extensibility, and testability. The original implementation tightly coupled the UserManager class to a concrete EmailService, making the system difficult to extend with alternative notification mechanisms and challenging to test in isolation.
By introducing abstractions and decoupling object creation from business logic, the refactored solution demonstrates how modern object-oriented design techniques can be used to address common architectural issues in small-scale applications while following established best practices.

2. Object-Oriented Principles and Techniques Used

Several core object-oriented principles and advanced design techniques were applied during the refactoring:
Dependency Inversion Principle (DIP)
The UserManager class was refactored to depend on an abstraction (NotificationService) rather than a concrete implementation (EmailService). This aligns with the Dependency Inversion Principle, which states that high-level modules should not depend on low-level modules but on abstractions (Martin, 2003).
Dependency Injection (DI)
Constructor injection was used to supply the NotificationService dependency to UserManager. This approach makes dependencies explicit and allows them to be easily substituted during testing or configuration.
Inversion of Control (IoC)
Object creation responsibility was moved outside the UserManager class. As a result, UserManager no longer controls which notification mechanism it uses, demonstrating Inversion of Control and improving flexibility.
Open/Closed Principle (OCP)
The system is now open for extension but closed for modification. New notification services, such as SMSService, can be added without modifying existing business logic.
Interface-Based Programming
An abstract base class (NotificationService) was introduced to define a common contract for all notification mechanisms, encouraging loose coupling and polymorphism.

3. Challenges Faced and How They Were Overcome

One of the main challenges was introducing the concept of interfaces in Python, a language that does not enforce interfaces in the same way as statically typed languages. This was addressed by using an abstract base class (ABC) to define a clear contract for notification services, ensuring consistent behaviour across implementations.
Another challenge involved distinguishing between unit testing and integration testing. Initially, testing the UserManagerrequired invoking the real email functionality, which was undesirable in unit tests. This was resolved by injecting a mock implementation of the NotificationService, allowing the UserManager to be tested in isolation. A separate integration test was then created to verify the behaviour of the actual EmailService.
Finally, ensuring compliance with SOLID principles while keeping the solution simple required careful separation of responsibilities, which was achieved by limiting each class to a single, well-defined purpose.

4. Demonstration of Advanced Object-Oriented Programming Concepts

The final artefact demonstrates an understanding of advanced object-oriented programming concepts by applying design principles typically used in larger, enterprise-level systems to a small Python application. The use of Dependency Injection and Inversion of Control shows an awareness of scalable architecture design and test-driven development practices.
Additionally, the separation of unit and integration tests reflects an understanding of professional software testing strategies. The optional use of a dependency injection container further demonstrates awareness of how object creation and configuration can be automated in more complex systems.
Overall, the refactored solution illustrates how advanced OOP concepts such as abstraction, polymorphism, and inversion of dependencies can significantly improve code quality, even in relatively simple applications.

References

Martin, R.C. (2003) Agile Software Development: Principles, Patterns, and Practices. Upper Saddle River, NJ: Prentice Hall.

Fowler, M. (2023) Inversion of Control Containers and the Dependency Injection Pattern. Available at: https://martinfowler.com/articles/injection.html 

Gamma, E., Helm, R., Johnson, R. and Vlissides, J. (2024) Design Patterns: Elements of Reusable Object-Oriented Software. 25th Anniversary Edition. Boston: Addison-Wesley.

Python Software Foundation (2024) unittest.mock — mock object library. Available at: https://docs.python.org/3/library/unittest.mock.html
