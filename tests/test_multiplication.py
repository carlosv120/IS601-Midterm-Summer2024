'''Testing Multiplication'''
import pytest
from app.plugins.multiplication import MultiplicationCommand
from app.plugins.csv import CsvCommand

@pytest.fixture
def csv_command():
    """Fixture to create a CsvCommand instance."""
    return CsvCommand()

@pytest.fixture
def multiplication_command(csv_command):
    """Fixture to create a MultiplicationCommand instance with a CsvCommand dependency."""
    return MultiplicationCommand(csv_command)

def test_multiply_success(multiplication_command, capfd):
    """Test the multiplication command with valid inputs."""
    multiplication_command.execute('2', '3')
    out = capfd.readouterr().out
    assert out.strip() == "The result of multiplying 2 and 3 is: 6"

def test_multiply_invalid_number(multiplication_command, capfd):
    """Test the multiplication command with one valid and one invalid input."""
    multiplication_command.execute('1.2', 'abc')
    out = capfd.readouterr().out
    assert out.strip() == "Invalid number input: 1.2 and/or abc is not a valid number. You are in the main menu."

def test_multiply_user_input_prompts(multiplication_command, monkeypatch, capfd):
    """Test the multiplication command prompts for user input when num1 and num2 are None."""
    inputs = iter(['4', '2'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    multiplication_command.execute()
    out = capfd.readouterr().out
    assert out.strip() == "The result of multiplying 4 and 2 is: 8"

def test_multiply_generic_exception(multiplication_command, capfd):
    """Test the multiplication command with a forced generic exception."""
    multiplication_command.execute('2', '3', raise_exception=True)
    out = capfd.readouterr().out
    assert "An error occurred: Forced exception for testing" in out.strip()
