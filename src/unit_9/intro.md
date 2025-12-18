Unit 9 Case Study

1. Purpose of the Task
The purpose of this task was to design and implement an online shopping system for the e-commerce company ShopEase using advanced object-oriented programming (OOP) principles in Python. The system was required to support scalability, modularity, security, and extensibility, which are critical requirements for modern e-commerce platforms that manage large volumes of users, products, and transactions.
To achieve this, the system was designed using a layered architecture, separating the presentation layer, business logic layer, and data access layer. Layered architectures are widely recommended for large systems as they improve maintainability, testability, and separation of concerns (Sommerville, 2024). The task also aimed to demonstrate the practical application of advanced OOP concepts and software design techniques through a realistic system artefact supported by unit testing.

Link to the full artifact:
https://github.com/jeffreywu2025/oop/tree/main/src/unit_9/shopease

2. Object-Oriented Principles and Techniques Used
The ShopEase system applies several fundamental and advanced object-oriented principles.
Encapsulation was implemented by grouping data and behaviour within cohesive classes such as AuthService and OrderService. Sensitive logic, including password handling and order processing, is hidden behind well-defined interfaces, reducing coupling and protecting internal state. Encapsulation is recognised as a core mechanism for managing complexity in large object-oriented systems (Sommerville, 2024).
Abstraction was achieved through the use of repository interfaces for users, products, and orders. These abstractions decouple business logic from data storage concerns, allowing the underlying persistence mechanism to be changed without affecting higher-level code. Such abstraction supports flexibility and long-term maintainability in evolving systems (Richards and Ford, 2024).
Polymorphism was demonstrated in the payment processing component. Multiple payment strategies (e.g. card and PayPal payments) implement a common interface, allowing them to be used interchangeably. This approach aligns with modern OOP practices that encourage substitutability and adherence to the Open–Closed Principle (Fowler, 2023).
In addition, established object-oriented design patterns were applied. A Factory-style approach was used to instantiate payment methods dynamically, while an Observer-based event mechanism was used to notify external components when orders are completed. Contemporary software engineering literature highlights the importance of such patterns for achieving extensibility and loose coupling in complex systems (Richards and Ford, 2024).

3. Challenges Faced and How They Were Overcome
One major challenge was designing a system that met all functional and non-functional requirements without introducing unnecessary complexity. This was addressed by adopting a layered architecture and ensuring each module had a clearly defined responsibility, reducing interdependencies between components (Sommerville, 2024).
Another challenge involved ensuring extensibility, particularly for features such as payment methods and notifications. This issue was resolved by using dependency injection and interface-based design, allowing new implementations to be added without modifying existing business logic. This technique is widely recognised as a best practice for building adaptable object-oriented systems (Richards and Ford, 2024).
Security was also a key concern, especially in relation to user authentication. Secure password hashing, salting, and constant-time comparison were used to protect user credentials. Encapsulating authentication logic within a dedicated service reduced the exposure of sensitive operations and aligned with recommended secure software design practices (Sommerville, 2024).
Finally, ensuring the system was testable presented a challenge. This was overcome by designing services to depend on abstractions rather than concrete implementations, enabling the use of in-memory repositories for unit testing. This approach allowed business logic to be tested independently of external infrastructure, improving reliability and development efficiency.

4. Demonstration of Advanced OOP Understanding
The ShopEase artefact demonstrates a strong understanding of advanced object-oriented programming concepts through its structured design, application of architectural principles, and emphasis on extensibility and testability.
The use of dependency injection illustrates an understanding of how loose coupling enhances maintainability and supports automated testing. The implementation of factory-based object creation and observer-style event handling shows the ability to apply object-oriented design techniques to real-world problems, such as dynamic feature extension and event-driven behaviour (Richards and Ford, 2024).
Furthermore, the abstraction of the data access layer and the inclusion of unit tests reflect professional software engineering practices. These features demonstrate awareness that modern object-oriented systems must be both scalable and verifiable, particularly in high-demand environments such as e-commerce platforms (Fowler, 2023; Sommerville, 2024).
Overall, the artefact effectively demonstrates the application of advanced OOP principles to create a secure, modular, and maintainable software system aligned with contemporary software engineering standards.


References:

Fowler, M. (2023) Refactoring: improving the design of existing code. 2nd edn. Boston: Addison-Wesley.

Richards, M. and Ford, N. (2024) Fundamentals of software architecture: an engineering approach. 2nd edn. Sebastopol: O’Reilly Media.

Sommerville, I. (2024) Software engineering. 11th edn. Harlow: Pearson Education.
