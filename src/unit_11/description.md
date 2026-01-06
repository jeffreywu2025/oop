Unit 11 Case study

1. Purpose of the Task

The purpose of this task was to refactor a simple Python application to apply Dependency Injection (DI) and Inversion of Control (IoC) principles in order to improve software maintainability, extensibility, and testability. The original implementation tightly coupled the UserManager class to a concrete EmailService, making the system difficult to extend with alternative notification mechanisms and challenging to test in isolation. By introducing abstractions and decoupling object creation from business logic, the refactored solution demonstrates how modern object-oriented design techniques can be applied to address common architectural issues in software development.

Link to the full artifact: https://github.com/jeffreywu2025/oop/tree/main/src/unit_11/coding

2. Object-Oriented Principles and Techniques Used

The refactored application applies several fundamental and advanced object-oriented programming principles. The Dependency Inversion Principle (DIP) was implemented by ensuring that the UserManager class depends on an abstraction (NotificationService) rather than a concrete implementation. This approach aligns with SOLID design principles, which recommend reducing coupling between high-level and low-level modules (Martin, 2003).

Dependency Injection (DI) was achieved through constructor injection, allowing the notification service to be supplied externally rather than instantiated internally. This supports Inversion of Control (IoC) by transferring responsibility for dependency creation outside the class, a widely recognised architectural pattern for improving modularity and testability (Fowler, 2023).

The refactoring also adheres to the Open/Closed Principle (OCP), as new notification mechanisms such as SMSService can be added without modifying existing business logic. Interface-based programming using an abstract base class further enables polymorphism and promotes loose coupling between components (Gamma et al., 2024).

3. Challenges Faced and How They Were Overcome

One challenge encountered during the refactoring process was implementing interface-like behaviour in Python, a language that does not enforce interfaces in the same way as statically typed languages. This issue was addressed by using an abstract base class to define a clear contract for notification services, ensuring consistent behaviour across implementations.

Another challenge involved separating unit tests from integration tests. Initially, testing the UserManager class required invoking the real email functionality, which introduced unnecessary side effects and reduced test reliability. This problem was resolved by injecting a mock implementation of the notification service during unit testing, allowing the UserManager to be tested in isolation. A separate integration test was then created to verify the behaviour of the actual EmailService, following best practices for software testing (Python Software Foundation, 2024).

4. Demonstration of Advanced Object-Oriented Programming Concepts

The final artefact demonstrates a clear understanding of advanced object-oriented programming concepts by applying industry-standard design principles to a simple Python application. The use of Dependency Injection and Inversion of Control illustrates an awareness of scalable and maintainable software architecture. Additionally, the separation of concerns between business logic and infrastructure services highlights effective use of abstraction and polymorphism.

The distinction between unit testing and integration testing further reflects an understanding of professional software development practices. Overall, the refactored solution shows how advanced object-oriented design techniques can significantly enhance code quality, extensibility, and testability, even within small-scale applications.

References

Martin, R.C. (2003) Agile Software Development: Principles, Patterns, and Practices. Upper Saddle River, NJ: Prentice Hall.

Fowler, M. (2023) Inversion of Control Containers and the Dependency Injection Pattern. 

Gamma, E., Helm, R., Johnson, R. and Vlissides, J. (2024) Design Patterns: Elements of Reusable Object-Oriented Software. 25th Anniversary Edition. Boston: Addison-Wesley.

Python Software Foundation (2024) unittest.mock — mock object library. 
