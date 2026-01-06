1.Overview
This project demonstrates the refactoring of a simple Python application to apply Dependency Injection (DI) and Inversion of Control (IoC) principles. The refactored design adheres to SOLID principles, improves maintainability, and significantly enhances testability by decoupling business logic from concrete service implementations.

2.Project Structure

coding/
│
├── user_management.py
├── test_user_manager_unit.py
├── test_email_service_integration.py
└── README.md

3.Description of Files
user_management.py
Contains the refactored application code:
* NotificationService abstract base class
* EmailService concrete implementation
* SMSService alternative implementation
* UserManager using constructor-based dependency injection

test_user_manager_unit.py
Unit test for UserManager:
* Uses a mock NotificationService
* Tests business logic in isolation
* Demonstrates the benefits of Dependency Injection

test_email_service_integration.py
Integration test for EmailService:
* Tests the real implementation without mocks
* Verifies observable behaviour of the service

4.Technologies Used
* Python 3.10+
* unittest.mock for mocking dependencies
* pytest for unit and integration testing

5.How to Run the Application

python user_management.py

6.How to Run the Tests

pytest -q

7.Key Design Principles Applied
* Dependency Injection (Constructor Injection)
* Inversion of Control
* SOLID Principles (DIP, OCP, SRP)
* Separation of Unit and Integration Testing
