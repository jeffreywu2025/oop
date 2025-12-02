#Unit 1 Coding Exercise

from abc import ABC, abstractmethod
import math

# -------------------------------------------------------------
# Task 1: Basic Class Hierarchy (Inheritance)
#
# Define a base class Vehicle with brand and fuel_type as instance
# attributes (use __init__).
# Create a subclass Car that inherits from Vehicle and adds num_doors
# as an additional attribute.
# Ensure the Car class calls the parent class's __init__ method
# (using super() in Python).
# -------------------------------------------------------------

class Vehicle:
    def __init__(self, brand, fuel_type):
        self.brand = brand
        self.fuel_type = fuel_type

    def __str__(self):
        return f"Vehicle(brand={self.brand}, fuel_type={self.fuel_type})"


class Car(Vehicle):
    def __init__(self, brand, fuel_type, num_doors):
        # Call parent constructor using super()
        super().__init__(brand, fuel_type)
        self.num_doors = num_doors

    def __str__(self):
        return (f"Car(brand={self.brand}, fuel_type={self.fuel_type}, "
                f"num_doors={self.num_doors})")


# -------------------------------------------------------------
# Task 2: Polymorphism with Methods
#
# Define an abstract Shape class with an abstract method area()
# (use ABC and abstractmethod in Python).
# Create Circle and Rectangle subclasses that inherit from Shape.
# Implement area() in each subclass (Circle: πr²; Rectangle: length*width).
# -------------------------------------------------------------

class Shape(ABC):
    @abstractmethod
    def area(self):
        pass


class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return math.pi * (self.radius ** 2)


class Rectangle(Shape):
    def __init__(self, length, width):
        self.length = length
        self.width = width

    def area(self):
        return self.length * self.width


# -------------------------------------------------------------
# Task 3: Encapsulation with Access Control
#
# Define BankAccount with a private attribute __balance (double underscore).
# Provide public methods:
#   deposit(amount) → adds to balance.
#   withdraw(amount) → deducts (check for sufficient funds).
# Provide getter get_balance() to return balance if needed.
# -------------------------------------------------------------

class BankAccount:
    def __init__(self, initial_balance=0.0):
        self.__balance = initial_balance  # private

    def deposit(self, amount):
        if amount <= 0:
            print("Deposit amount must be positive.")
            return
        self.__balance += amount
        print(f"Deposited {amount}. New balance: {self.__balance}")

    def withdraw(self, amount):
        if amount <= 0:
            print("Withdrawal amount must be positive.")
            return
        if amount > self.__balance:
            print("Insufficient funds.")
            return
        self.__balance -= amount
        print(f"Withdrew {amount}. New balance: {self.__balance}")

    def get_balance(self):
        return self.__balance


# -------------------------------------------------------------
# Task 4: Abstraction with Base Class
#
# Create an abstract Animal class with an abstract make_sound() method.
# Implement Dog and Cat subclasses that override make_sound() to return
# "Woof!" and "Meow!" respectively.
# -------------------------------------------------------------

class Animal(ABC):
    @abstractmethod
    def make_sound(self):
        pass


class Dog(Animal):
    def make_sound(self):
        return "Woof!"


class Cat(Animal):
    def make_sound(self):
        return "Meow!"


# -------------------------------------------------------------
# Task 5: Constructor and Destructor
#
# Define a Person class with __init__(self, name) to set name.
# Add a destructor __del__(self) that prints "Goodbye, {name}!".
# Test by creating and deleting an instance.
# -------------------------------------------------------------

class Person:
    def __init__(self, name):
        self.name = name
        print(f"Person {self.name} has been created.")

    def __del__(self):
        print(f"Goodbye, {self.name}!")


# -------------------------------------------------------------
# Simple tests / demonstration
# -------------------------------------------------------------
if __name__ == "__main__":
    print("=== Task 1: Vehicle & Car ===")
    v = Vehicle("GenericBrand", "diesel")
    c = Car("Toyota", "petrol", 4)
    print(v)
    print(c)

    print("\n=== Task 2: Shape, Circle, Rectangle ===")
    shapes = [Circle(3), Rectangle(4, 5)]
    for s in shapes:
        print(f"{s.__class__.__name__} area:", s.area())

    print("\n=== Task 3: BankAccount ===")
    acc = BankAccount(100)
    acc.deposit(50)
    acc.withdraw(30)
    acc.withdraw(1000)
    print("Final balance:", acc.get_balance())

    print("\n=== Task 4: Animal sounds ===")
    animals = [Dog(), Cat()]
    for a in animals:
        print(f"{a.__class__.__name__}:", a.make_sound())

    print("\n=== Task 5: Person constructor & destructor ===")
    p = Person("Alice")
    del p

    print("\nEnd of demo.")
