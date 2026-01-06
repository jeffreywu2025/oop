Unit 12 Capstone Project Description: AI-Driven Intrusion Detection System (IDS)

1. Problem Statement

Modern information systems are increasingly exposed to credential-based attacks such as brute-force login attempts, credential stuffing, and anomalous authentication behaviour. These attacks frequently bypass traditional signature-based intrusion detection systems (IDS), which rely on predefined rules and known attack patterns. Consequently, malicious activities that exhibit novel or adaptive characteristics often remain undetected (Rahman and Shakil, 2023).

The core problem addressed by this capstone project is the lack of adaptive yet explainable intrusion detection mechanisms capable of identifying both known and previously unseen authentication-based threats while remaining transparent, testable, and maintainable.

2. Purpose of the Task

The purpose of this capstone project is to design and implement an AI-driven Intrusion Detection System (IDS) that focuses on authentication security by analysing login events in real time. The system aims to:

2.1 Monitor authentication activity continuously

2.2 Detect suspicious behaviour using both deterministic rules and machine-learning techniques

2.3 Respond automatically through configurable security actions
A hybrid IDS approach was selected because recent research demonstrates that combining rule-based logic with machine-learning anomaly detection provides improved coverage and robustness compared to single-method systems (Alqahtani, Alenezi and Mustafa, 2024).

3. Design Decisions

3.1 Hybrid Detection Strategy
A major design decision was the adoption of a hybrid detection model. Rule-based detection enables the identification of well-understood attack patterns such as repeated failed login attempts or access from blacklisted IP addresses. In contrast, machine-learning-based anomaly detection identifies deviations from normal behaviour without relying on predefined signatures (Chen, Rahimi and Botros, 2023).
This combination ensures both explainability and adaptability, which are essential characteristics of modern IDS solutions.

3.2 Event-Driven Architecture
The system was designed using an event-driven architecture, where all security-relevant activities are represented as structured events. Events are distributed via a central event-handling mechanism, allowing producers and consumers to remain loosely coupled.
Event-driven designs are increasingly adopted in cybersecurity systems due to their scalability, modularity, and suitability for real-time analysis (Wu, Singh and Patel, 2024).

3.3 Object-Oriented Modular Design

The IDS was implemented using object-oriented programming (OOP) principles to enhance maintainability and extensibility. Key principles applied include:

3.3.1 Single Responsibility Principle – each module performs a clearly defined role

3.3.2 Open/Closed Principle – new detectors or actions can be added without modifying existing code

3.3.3 Dependency Injection – external services and models are injected to improve testability

These design choices align with modern secure software engineering guidelines (NIST, 2024).

4. Implementation Overview

4.1 Event and Data Source Implementation
The system defines structured event representations for authentication activity. Two data sources are implemented:

4.1.1 A simulated data source, which generates synthetic login events for testing and demonstration

4.1.2 A log file data source, which replays historical authentication logs for reproducibility
Synthetic data generation and log replay are widely recommended practices in IDS development and evaluation (Sosa and Mendoza, 2023).

4.2 Detection Layer Implementation

4.2.1 Rule-Based Detection
Rule-based detection is implemented through independent rule components that evaluate login events against predefined conditions, such as rapid failed login bursts or suspicious IP usage. These rules provide deterministic and interpretable detection outcomes, supporting security auditing and incident analysis (Liang and Sang, 2024).

4.2.2 Machine-Learning Detection
The machine-learning component employs an unsupervised anomaly detection model based on Isolation Forest, implemented using the scikit-learn library. Isolation Forest is well suited to authentication anomaly detection due to its efficiency and ability to detect outliers without labelled training data (Ortega and Sun, 2025).

The model trains automatically once sufficient behavioural data has been collected, and internal safeguards ensure predictions are only generated after successful training.

4.3 Controller and Response Actions

A central controller coordinates event processing, detection logic, and system responses. When suspicious behaviour is detected, the system can trigger one or more automated actions, including:

4.3.1 Logging security events

4.3.2 Raising alerts

4.3.3 Blocking suspicious IP addresses 4.3.4 Sending notification emails

Response actions are implemented as independent components, allowing the system to be easily extended with additional mitigation strategies (Alqahtani, Alenezi and Mustafa, 2024).

5. Conclusion

This capstone project provides a modular, extensible, and academically grounded Intrusion Detection System that addresses the shortcomings of traditional signature-based IDS solutions. By integrating rule-based logic with machine-learning anomaly detection, the system is capable of identifying both known and previously unseen authentication threats.

The project demonstrates informed design decisions, effective application of object-oriented principles, and alignment with recent research in cybersecurity and secure software engineering.

References

Alqahtani, F., Alenezi, M. and Mustafa, A. (2024) Hybrid intrusion detection systems: Enhancing anomaly detection using combined rule-based and machine-learning approaches. Computers & Security, 140, pp. 103–119.

Chen, L., Rahimi, R. and Botros, T. (2023) Evaluating lightweight anomaly detection models for login security monitoring. Journal of Cybersecurity Research, 15(2), pp. 88–102.

Liang, J. and Sang, D. (2024) Policy-based detection in modern authentication systems: A rule-driven evaluation. International Journal of Information Security Science, 13(1), pp. 44–59.

NIST (2024) Secure Software Development Framework (SSDF) Version 1.2. National Institute of Standards and Technology.

Ortega, A. and Sun, Y. (2025) Advances in Isolation Forest for security anomaly detection. ACM Transactions on Cybersecurity, 8(1), pp. 1–22.

Rahman, M. and Shakil, S. (2023) A systematic review of hybrid rule–machine-learning intrusion detection models. IEEE Access, 11, pp. 65432–65467.

Sosa, M. and Mendoza, F. (2023) Synthetic event generation for IDS evaluation: Techniques and challenges. Journal of Information Assurance, 19(4), pp. 75–92.

Wu, H., Singh, A. and Patel, C. (2024) Event-driven pipelines for scalable cybersecurity analytics. ACM SIGSAC Review, 12(3), pp. 33–49.
