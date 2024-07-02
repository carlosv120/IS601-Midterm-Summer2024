'''Testing Addition'''
import pytest
from app.plugins.addition import AdditionCommand
from app.plugins.csv import CsvCommand

@pytest.fixture
def csv_command():
    """Fixture to create a CsvCommand instance."""
    return CsvCommand()

@pytest.fixture
def addition_command(csv_command):
    """Fixture to create an AdditionCommand instance with a CsvCommand dependency."""
    return AdditionCommand(csv_command)

def test_add_success(addition_command, capfd):
    """Test the addition command with valid inputs."""
    addition_command.execute('2', '3')
    out = capfd.readouterr().out
    assert out.strip() == "The result of adding 2 and 3 is: 5"

def test_add_invalid_number(addition_command, capfd):
    """Test the addition command with one valid and one invalid input."""
    addition_command.execute('1.1', 'abc')
    out = capfd.readouterr().out
    assert out.strip() == "Invalid number input: 1.1 and/or abc is not a valid number. You are in the main menu."

def test_add_user_input_prompts(addition_command, monkeypatch, capfd):
    """Test the addition command prompts for user input when num1 and num2 are None."""
    inputs = iter(['4', '5'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    addition_command.execute()
    out = capfd.readouterr().out
    assert out.strip() == "The result of adding 4 and 5 is: 9"

def test_add_generic_exception(addition_command, capfd):
    """Test the addition command with a forced generic exception."""
    addition_command.execute('2', '3', raise_exception=True)
    out = capfd.readouterr().out
    assert "An error occurred: Forced exception for testing" in out.strip()
