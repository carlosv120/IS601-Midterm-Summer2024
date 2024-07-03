'''Testing DivisionCommand'''
import pytest
from app.plugins.division import DivisionCommand
from app.plugins.csv import CsvCommand

@pytest.fixture
def csv_command():
    """Fixture to create a CsvCommand instance."""
    return CsvCommand()

@pytest.fixture
def division_command(csv_command):
    """Fixture to create a DivisionCommand instance with a CsvCommand dependency."""
    return DivisionCommand(csv_command)

def test_divide_invalid_number(division_command, capfd):
    """Test the division command with one valid and one invalid input."""
    division_command.execute('1.1', 'abc')
    out = capfd.readouterr().out
    assert out.strip() == "Invalid number input: 1.1 and/or abc is not a valid number. You are in the main menu."

def test_divide_user_input_prompts(division_command, monkeypatch, capfd):
    """Test the division command prompts for user input when num1 and num2 are None."""
    inputs = iter(['6', '2'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    division_command.execute()
    out = capfd.readouterr().out
    assert out.strip() == "The result of dividing 6 by 2 is: 3"

def test_divide_by_zero(division_command, capfd):
    """Testing the divide by zero"""
    division_command.execute('10', '0')
    out = capfd.readouterr().out
    assert out.strip() == "Cannot divide by zero. You are in the main menu."

def test_divide_generic_exception(division_command, capfd):
    """Test the division command with a forced generic exception."""
    division_command.execute('6', '3', raise_exception=True)
    out = capfd.readouterr().out
    assert "An error occurred: Forced exception for testing" in out.strip()
