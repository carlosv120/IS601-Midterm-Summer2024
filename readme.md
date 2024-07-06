# Midterm IS - 601 Introduction to Web Development Systems

In this Readme file, you will find all the midterm requirements that come along with the code, including descriptions and implementation examples of different concepts learned throughout the course. The link to the video will be located at the end of this document.

## Design Patterns

### Creational Patterns: Factory Method.

**Description:** Factory Method is a creational design pattern that provides an interface for creating objects in a superclass but allows subclasses to alter the type of objects that will be created ([Refactoring Guru, 2024](https://refactoring.guru/design-patterns/factory-method)).

**Implementation:** In the `Calculator class`, we use a dynamic plugin loading mechanism to register command objects. This acts as a factory for creating and initializing different command objects.

**Example:** [Calculator Class. Line 39: load_plugins](https://github.com/carlosv120/IS601-Midterm-Summer2024/blob/main/app/__init__.py)

### Behavioral Patterns: Command Pattern

**Description:** The Command Pattern is a behavioral design pattern that turns a request into a stand-alone object that contains all information about the request. This transformation lets you pass requests as a method arguments, delay or queue a request’s execution, and support undoable operations. ([Refactoring Guru, 2024](https://refactoring.guru/design-patterns/command)).

**Implementation:** The entire command structure, with the best example being the `MenuCommand` is a clear use of this pattern, including the `AdditionCommand`, `DivisionCommand`, `SubtractionCommand`, etc. Each command encapsulates a specific operation and can be executed independently.

**Example:** ([BaseCommand Class. Line 8:](https://github.com/carlosv120/IS601-Midterm-Summer2024/blob/main/app/commands/__init__.py)).

**Example:** ([AdditionCommand Class. Line 5:](https://github.com/carlosv120/IS601-Midterm-Summer2024/blob/main/app/plugins/addition/__init__.py)).

## Environment Variables

**Description:** Environment variables allow you to change configuration settings without modifying the application’s code. This is particularly useful in scenarios where configurations need to be adjusted frequently or on-the-fly. They allow you to manage configuration settings for your application without hardcoding values in your code. ([Medium, 2022](https://medium.com/@suchitra9049/rails-7-setting-environment-variables-using-dotenv-rails-9457a10ec958)).

**Implementation:** Environment variables are loaded using the `dotenv` package and are used to configure settings in the application.

**Example:** ([Calculator Class. Line 31: load_environment_variables](https://github.com/carlosv120/IS601-Midterm-Summer2024/blob/main/app/__init__.py)).

## Logging Practices

**Description:** Logging is used to record significant events in the application, which helps in debugging and monitoring the application's behavior. ([Java Challengers, 2021](https://javachallengers.com/logging-and-monitoring/#:~:text=Logging%20is%20the%20process%20of,about%20system%20performance%20and%20usage)).

**Implementation:** Logging is configured in the Calculator class and used all over the application to log important events, such as initialization, errors, and significant operations.

**Configuration:** ([Calculator Class. Line 23: configure_logging](https://github.com/carlosv120/IS601-Midterm-Summer2024/blob/main/app/__init__.py)).

**Example:** ([AdditionCommand Class. Line 10, 13, 16:](https://github.com/carlosv120/IS601-Midterm-Summer2024/blob/main/app/plugins/addition/__init__.py)).


## Exception Handling

### Look Before You Leap (LBYL)

**Description:** This coding style explicitly tests for pre-conditions before making calls or lookups. `If` statements are common for this style of coding.  ([Python Glosary Terms, 2024](https://docs.python.org/3/glossary.html#term-LBYL)).

**Implementation:** Before reading the CSV file, the code checks if the file exists and is accessible.

**Example:** ([CsvCommand Class. Line 16: load_existing_history ](https://github.com/carlosv120/IS601-Midterm-Summer2024/blob/main/app/plugins/csv/__init__.py)).

### Easier to Ask for Forgiveness than Permission (EAFP)

**Description:** This coding style assumes the existence of valid keys or attributes and catches exceptions if the assumption proves false. This clean and fast style is characterized by the presence of many try and except statements.  ([Phyton Glossary Terms, 2024](https://docs.python.org/3/glossary.html#term-EAFP)).

**Implementation:** When saving to the CSV file, the code tries to write and catches exceptions if the operation fails.

**Example:** ([CsvCommand Class. Line 44: save_to_csv ](https://github.com/carlosv120/IS601-Midterm-Summer2024/blob/main/app/plugins/csv/__init__.py)).

## Video demonstration

**Link:** 
