'''Testing Subtraction'''
import pytest
from app.plugins.subtraction import SubtractionCommand
from app.plugins.csv import CsvCommand

@pytest.fixture
def csv_command():
    """Fixture to create a CsvCommand instance."""
    return CsvCommand()

@pytest.fixture
def subtraction_command(csv_command):
    """Fixture to create a SubtractionCommand instance with a CsvCommand dependency."""
    return SubtractionCommand(csv_command)

def test_subtract_success(subtraction_command, capfd):
    """Test the subtraction command with valid inputs."""
    subtraction_command.execute('5', '3')
    out = capfd.readouterr().out
    assert out.strip() == "The result of subtracting 3 from 5 is: 2"

def test_subtract_invalid_number(subtraction_command, capfd):
    """Test the subtraction command with one valid and one invalid input."""
    subtraction_command.execute('1.1', 'abc')
    out = capfd.readouterr().out
    assert out.strip() == "Invalid number input: 1.1 and/or abc is not a valid number. You are in the main menu."

def test_subtract_user_input_prompts(subtraction_command, monkeypatch, capfd):
    """Test the subtraction command prompts for user input when num1 and num2 are None."""
    inputs = iter(['4', '2'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    subtraction_command.execute()
    out = capfd.readouterr().out
    assert out.strip() == "The result of subtracting 2 from 4 is: 2"

def test_subtract_generic_exception(subtraction_command, capfd):
    """Test the subtraction command with a forced generic exception."""
    subtraction_command.execute('2', '3', raise_exception=True)
    out = capfd.readouterr().out
    assert "An error occurred: Forced exception for testing" in out.strip()
