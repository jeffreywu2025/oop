"""
TASK (Factory Method Pattern – Car Manufacturing System)

You are designing a system for a car manufacturing company that produces
different types of cars (Sedan, SUV, Hatchback). The goal is to create a
flexible solution where the main program does NOT need to know the exact
car classes it is instantiating. Instead, the Factory Method Pattern will
be used to delegate object creation to subclasses.

REQUIREMENTS:
1. A Car interface or abstract class with a drive() method.
2. Concrete car classes (Sedan, SUV, Hatchback) implementing Car.
3. A CarFactory abstract class defining the factory method create_car().
4. Concrete factory classes (SedanFactory, SUVFactory, HatchbackFactory).
5. A demonstration showing how different cars are created and driven
   using the factory method pattern.

EXPLANATION (≈300 words):

The Factory Method Pattern provides a clean approach for separating object
creation from usage. Instead of instantiating car types directly in the
main program (e.g., Sedan(), SUV()), we define an abstract CarFactory
with a factory method create_car(). This method is implemented differently
in concrete factory classes such as SedanFactory or SUVFactory. As a
result, the client code depends only on the abstract Car and CarFactory,
not the specific car implementations, satisfying the Open/Closed Principle
of software design.

Each car type extends the Car interface by implementing the drive()
method. This enforces consistent behavior across all car types while
still allowing each class to define its unique driving characteristics.
The factories encapsulate creation logic so the program can introduce new
car types without modifying existing code—only new factory and product
classes need to be added.

In the demonstration, the main program iterates over a list of factories
to create and drive cars. It does not know whether each factory is
producing a Sedan, SUV, or Hatchback. This decoupling enhances
maintainability and scalability, making the system adaptable to future
car types with minimal changes.

"""


from abc import ABC, abstractmethod

# === Product abstraction ===
class Car(ABC):
    @abstractmethod
    def drive(self) -> str:
        """Return a driving message specific to the car type."""
        pass


# === Concrete products ===
class Sedan(Car):
    def drive(self) -> str:
        return "Sedan: smooth ride, great fuel economy."


class SUV(Car):
    def drive(self) -> str:
        return "SUV: high clearance, spacious interior."


class Hatchback(Car):
    def drive(self) -> str:
        return "Hatchback: compact size, versatile cargo."


# === Creator abstraction ===
class CarFactory(ABC):
    @abstractmethod
    def create_car(self) -> Car:
        """Factory Method that returns a Car."""
        pass

    def deliver(self) -> str:
        """Optional hook: shared post-creation logic."""
        car = self.create_car()
        return f"Delivering -> {car.drive()}"


# === Concrete creators ===
class SedanFactory(CarFactory):
    def create_car(self) -> Car:
        return Sedan()


class SUVFactory(CarFactory):
    def create_car(self) -> Car:
        return SUV()


class HatchbackFactory(CarFactory):
    def create_car(self) -> Car:
        return Hatchback()


# === Client code ===
def main():
    factories: list[CarFactory] = [
        SedanFactory(), SUVFactory(), HatchbackFactory()
    ]

    for factory in factories:
        car = factory.create_car()
        print(car.drive())
        print(factory.deliver())
        print("-" * 40)


if __name__ == "__main__":
    main()
