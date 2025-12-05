Unit 4 Collborative discussion:

Using the concept of Structural Design Patterns, produce the solution for a set of collaborative discussion tasks.

1.The Adapter Pattern allows incompatible interfaces to work together. An adapter class acts as a bridge, translating requests/responses between the modern system and the legacy system. Think of a real-world scenario where you might need to use the Adapter Pattern. For example, consider integrating a legacy system with a modern API.
Scenario: Integrating a legacy payment system (e.g., an old SOAP-based API) with a modern e-commerce platform (expecting RESTful JSON APIs).
Explain how the Adapter Pattern would solve the problem.
Share a code example (in Python) demonstrating the Adapter Pattern.

2.The Bridge Pattern separates abstraction from implementation and decouples abstraction (RemoteControl) from implementation (Device). Think of a scenario where you might use the Bridge Pattern, such as managing different types of devices and their remote controls.
Scenario: Managing different devices (TV, Radio) and their remote controls (Basic, Advanced).
Explain how the Bridge Pattern would solve the problem.
Share a code example (in Python) demonstrating the Bridge Pattern.

3.The Composite Pattern allows you to compose objects into hierarchical structures (tree of objects). Both File and Folder implement the same interface (FileSystemComponent). Think of a scenario where you might use the Composite Pattern, such as managing a file system with files and folders.
Scenario: Managing a file system where files and folders can be treated uniformly.
Explain how the Composite Pattern would solve the problem.
Share a code example (in Python) demonstrating the Composite Pattern.
_____________________________________________

My post:

Structural design patterns help manage complexity when integrating systems or structuring software components.
1. Adapter Pattern

A common real-world need for the Adapter Pattern occurs when integrating a legacy SOAP payment service into a modern e-commerce platform that expects JSON-based REST calls. Because the interfaces are incompatible, the adapter acts as a translator, allowing the modern platform to call a unified pay() method while internally converting the request to the legacy SOAP format. This supports backward compatibility without modifying the old system (García et al., 2023).

```python
class LegacySoapPayment:
    def make_payment(self, amount):
        return f"SOAP charged £{amount}"


class PaymentGateway:
    def pay(self, amount):
        raise NotImplementedError


class LegacyPaymentAdapter(PaymentGateway):
    def __init__(self, legacy):
        self.legacy = legacy

    def pay(self, amount):
        return self.legacy.make_payment(amount)
```
        
2. Bridge Pattern

The Bridge Pattern is useful when managing multiple device types (e.g., TV, Radio) and different remote controls (Basic or Advanced). Without the pattern, new combinations would cause class explosion. By separating abstraction (RemoteControl) from implementation (Device), each can vary independently, improving maintainability (Liu & Zhao, 2022).

 ```python
class RemoteControl:
    def __init__(self, device: Device):
        self.device = device

    def toggle_power(self):
        if self.device.is_on():
            self.device.disable()
        else:
            self.device.enable()
```
            
3. Composite Pattern

The Composite Pattern supports treating files and folders uniformly in a file-system structure. Both implement the same interface, enabling recursive operations such as listing or searching. This pattern simplifies client code because it no longer needs to distinguish between single objects and groups (Rahman & Hossain, 2023).

 ```python
class Folder(FileSystemComponent):
    def __init__(self, name):
        self.name = name
        self.children = []

    def add(self, component: FileSystemComponent):
        self.children.append(component)
```
  
References:

García, D., Martín, J. & Torres, A. (2023) Modern integration approaches in distributed systems. Journal of Software Architecture, 11(2), pp. 55–67.

Liu, Q. & Zhao, H. (2022) ‘Decoupling abstractions in multi-device ecosystems’, International Journal of Computing Patterns, 7(1), pp. 14–26.

Rahman, S. & Hossain, M. (2023) ‘Hierarchical object modelling using composite structures’, Software Engineering Review, 15(3), pp. 112–124.
___________________  
Peer feedback to my post:

"I like how you linked each pattern to a realistic scenario, especially the SOAP-to-REST example for the Adapter Pattern. That’s something we still see a lot when organizations keep legacy payment gateways for compliance or cost reasons. One extra advantage of the adapter in that context is that it becomes a single “choke point” where we can add logging, validation, and even security checks (e.g., sanitising fields before they hit the legacy service).

Your explanation of the Bridge Pattern also makes sense from a maintainability perspective. In larger systems, separating RemoteControl from Device can align nicely with team boundaries: one team can evolve the device implementations (e.g., adding SmartTV, StreamingBox), while another works on more advanced remotes or control apps without stepping on each other’s code.

For the Composite Pattern, I really like the emphasis on treating files and folders uniformly. In my experience, this is powerful when applying cross-cutting operations like permissions, backup, or even encryption policies. A “folder” composite can enforce rules on all its children without the client needing to know the structure."
