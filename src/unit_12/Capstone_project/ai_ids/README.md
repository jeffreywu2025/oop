# AI-Driven Intrusion Detection System (IDS)

## Overview

This project implements an AI-Driven Intrusion Detection System (IDS) designed to detect suspicious authentication behaviour using a hybrid detection approach that combines rule-based logic with machine-learning-based anomaly detection.

The system focuses on login event monitoring and is implemented in Python using a modular, object-oriented architecture. It is designed to be extensible, testable, and academically demonstrative of advanced software engineering and OOP principles.

---

## Key Features

- Real-time processing of authentication (`LoginEvent`) data
- Hybrid detection strategy:
  - Rule-based detection for known attack patterns
  - Machine-learning anomaly detection using `IsolationForest`
- Event-driven architecture using a central `EventBus`
- Configurable security settings via `SecurityConfig`
- Automated response actions (alerts, logging, IP blocking, email notifications)
- Fully unit-tested with dependency injection for safe testing

---

## Project Structure

ai_ids/
│
├── actions/
│ └── actions.py # AlertAction, LogAction, BlockIPAction, EmailAlertAction
│
├── controller/
│ ├── core.py # IDSController
│ ├── config.py # SecurityConfig
│ └── event_bus.py # EventBus
│
├── datasource/
│ ├── simulated_source.py # SimulatedDataSource
│ └── log_file_source.py # LogFileDataSource
│
├── detectors/
│ ├── base.py # DetectionResult, SklearnAnomalyModel, DummyAnomalyModel
│ ├── rules.py # RuleBasedDetector and rule classes
│ └── ml.py # MLAnomalyDetector
│
├── events/
│ └── base.py # Event, LoginEvent, NetworkEvent, SystemEvent
│
├── security/
│ ├── auth.py # Authentication utilities (e.g. AuthService)
│ └── validation.py # Input validation (validate_username, validate_ip)
│
├── tests/
│ ├── test_detectors.py
│ ├── test_controller.py
│ └── test_email_action.py
│
└── main.py # Application entry point

## Running the Application

### Prerequisites

- Python 3.10+
- Optional: `scikit-learn` (for ML anomaly detection)

Install dependencies (if applicable):

pip install scikit-learn

## Run the IDS
python ai_ids/main.py

By default, the system can be configured to use either:
SimulatedDataSource (synthetic login events), or
LogFileDataSource (log replay)

## Testing

The project includes a unit test suite located in the tests/ directory:
test_detectors.py – tests rule-based and ML detection logic
test_controller.py – tests controller integration and action triggering
test_email_action.py – tests email alerts using a mock sender

Run tests with:
pytest

## Object-Oriented Design
This project demonstrates advanced OOP concepts, including:

-Inheritance (Event base class and subclasses)

-Polymorphism (detectors, ML models, actions)

-Encapsulation (internal state, configuration, ML flags)

-Composition (controller → detectors → actions)

-Strategy Pattern (rules and ML models)

-Observer Pattern (EventBus subscribers)

-Dependency Injection (email sender, ML models)

-Open/Closed Principle (extensible rules and actions)

