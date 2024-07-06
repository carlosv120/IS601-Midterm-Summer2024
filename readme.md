# Midterm IS - 601 Introduction to Web Development Systems

## Design Patterns

### Creational Patterns: Factory Method.

**Description:** Factory Method is a creational design pattern that provides an interface for creating objects in a superclass but allows subclasses to alter the type of objects that will be created [Refactoring Guru, 2024](https://refactoring.guru/design-patterns/factory-method)
.

**Implementation:** In the `Calculator class`, we use a dynamic plugin loading mechanism to register command objects. This acts as a factory for creating and initializing different command objects.

**Example:** [Calculator Class. Line 39: load_plugins](https://github.com/carlosv120/IS601-Midterm-Summer2024/blob/main/app/__init__.py)

