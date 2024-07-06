'''Testing CsvCommand'''
import logging
from unittest.mock import patch, mock_open
import pytest
import pandas as pd
from app.plugins.csv import CsvCommand

@pytest.fixture
def csv_command():
    """Fixture to create a CsvCommand instance."""
    with patch('builtins.open', mock_open(read_data="operation,num1,num2,result\naddition,2,3,5\n")):
        with patch('pandas.read_csv') as mock_read_csv:
            mock_read_csv.return_value = pd.DataFrame([{'operation': 'addition', 'num1': '2', 'num2': '3', 'result': '5'}])
            return CsvCommand()

def test_load_history(csv_command, caplog):
    """Test loading the calculation history."""
    with caplog.at_level(logging.INFO):
        csv_command.load_existing_history()
    assert "Existing calculation history loaded from" in caplog.text

def test_load_history_empty_data_error(caplog):
    """Test loading the calculation history with EmptyDataError."""
    with patch('os.path.exists', return_value=True):
        with patch('pandas.read_csv', side_effect=pd.errors.EmptyDataError):
            with caplog.at_level(logging.INFO):
                CsvCommand.load_existing_history()
    assert "No data found in 'data/calculation_history.csv'. Initialized with empty history." in caplog.text

def test_load_history_general_exception(caplog):
    """Test loading the calculation history with a general exception."""
    with patch('os.path.exists', return_value=True):
        with patch('pandas.read_csv', side_effect=Exception("General error")):
            with caplog.at_level(logging.ERROR):
                CsvCommand.load_existing_history()
    assert "Failed to read existing CSV file: General error" in caplog.text

def test_execute_delete_no_calculations(csv_command, monkeypatch, capfd, caplog):
    """Test the execute method with delete command when no calculations are available."""
    # Clear any existing calculations
    csv_command.clear_history()
    inputs = iter(['delete', 'back'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    with caplog.at_level(logging.INFO):
        csv_command.execute()
    out = capfd.readouterr().out
    assert "No calculations available to delete." in out

def test_add_calculation(csv_command):
    """Test adding a calculation."""
    csv_command.add_calculation('addition', '2', '3', '5')
    assert csv_command.calculation_history[-1] == {'operation': 'addition', 'num1': '2', 'num2': '3', 'result': '5'}

def test_save_to_csv_failure(csv_command, caplog):
    """Test saving the calculation history with a failure."""
    with patch('pandas.DataFrame.to_csv', side_effect=Exception("Failed to write")):
        with caplog.at_level(logging.ERROR):
            csv_command.add_calculation('addition', '2', '3', '5')
    assert "Failed to write CSV file" in caplog.text

def test_clear_history(csv_command):
    """Test clearing the calculation history."""
    csv_command.clear_history()
    assert csv_command.calculation_history == []

def test_delete_calculation(csv_command, caplog):
    """Test deleting a calculation."""
    csv_command.add_calculation('addition', '2', '3', '5')
    with caplog.at_level(logging.INFO):
        csv_command.delete_calculation(0)
    assert "Calculation at index 0 deleted." in caplog.text

def test_invalid_delete_index(csv_command, caplog):
    """Test deleting a calculation with an invalid index."""
    csv_command.add_calculation('addition', '2', '3', '5')
    with caplog.at_level(logging.WARNING):
        csv_command.delete_calculation(10)
    assert "Invalid index 10. Cannot delete calculation." in caplog.text

def test_execute_load(csv_command, monkeypatch, capfd):
    """Test the execute method with load command."""
    inputs = iter(['load', 'back'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    csv_command.execute()
    out = capfd.readouterr().out
    assert "Calculation History from CSV:" in out

def test_execute_clear(csv_command, monkeypatch, capfd):
    """Test the execute method with clear command."""
    inputs = iter(['clear', 'back'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    csv_command.execute()
    out = capfd.readouterr().out
    assert "Calculation history cleared." in out

def test_execute_delete(csv_command, monkeypatch, caplog, capfd):
    """Test the execute method with delete command."""
    csv_command.add_calculation('addition', '2', '3', '5')
    inputs = iter(['delete', '0', 'back'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    with caplog.at_level(logging.INFO):
        csv_command.execute()
    assert "Calculation at index 0 deleted." in caplog.text

def test_execute_invalid_command(csv_command, monkeypatch, capfd):
    """Test the execute method with an invalid command."""
    inputs = iter(['invalid', 'back'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    csv_command.execute()
    out = capfd.readouterr().out
    assert "Invalid command. Please enter 'load', 'clear', 'delete', or 'back'." in out
    assert "You are in the main menu" in out
