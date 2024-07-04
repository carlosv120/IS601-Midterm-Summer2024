import logging
import os
from app.commands import Command
import pandas as pd

class CsvCommand(Command):
    calculation_history = []
    data_dir = 'data'
    csv_file_path = os.path.join(data_dir, 'calculation_history.csv')

    def __init__(self):
        self.load_existing_history()
        logging.info("CsvCommand initialized.")

    @classmethod
    def load_existing_history(cls):
        if os.path.exists(cls.csv_file_path):
            df_existing_history = pd.read_csv(cls.csv_file_path)
            cls.calculation_history = df_existing_history.to_dict('records')
            logging.info(f"Existing calculation history loaded from '{cls.csv_file_path}'.")

    @classmethod
    def add_calculation(cls, operation, num1, num2, result):
        cls.calculation_history.append({
            'operation': operation,
            'num1': num1,
            'num2': num2,
            'result': result
        })
        cls.save_to_csv()
        logging.info(f"Calculation added: {operation}({num1}, {num2}) = {result}")
        cls.print_calculation_history()

    @classmethod
    def save_to_csv(cls):
        if not os.path.exists(cls.data_dir):
            os.makedirs(cls.data_dir)
            logging.info(f"The directory '{cls.data_dir}' is created.")
        elif not os.access(cls.data_dir, os.W_OK):
            logging.error(f"The directory '{cls.data_dir}' is not writable.")
            return

        df_history = pd.DataFrame(cls.calculation_history)
        try:
            df_history.to_csv(cls.csv_file_path, index=False)
            logging.info(f"Calculation history saved to CSV at '{cls.csv_file_path}'.")
        except Exception as e:
            logging.error(f"Failed to write CSV file: {e}")

    @classmethod
    def clear_history(cls):
        '''Clears the history of calculations'''
        cls.calculation_history.clear()
        cls.save_to_csv()
        logging.info("Calculation history cleared.")

    @classmethod
    def delete_calculation(cls, index):
        '''Deletes a calculation by index'''
        if 0 <= index < len(cls.calculation_history):
            del cls.calculation_history[index]
            cls.save_to_csv()
            logging.info(f"Calculation at index {index} deleted.")
        else:
            logging.warning(f"Invalid index {index}. Cannot delete calculation.")

    @classmethod
    def execute(cls):
        print("CSV Command Menu:\n" + '-' * 120)
        print("load ---- clear ---- delete ---- back")
        print('-' * 120)
        print("Type 'back' to return to the main menu.")
        logging.info("CSV Command Menu displayed.")
        
        while True:
            choice = input("Enter a csv command: ").strip().lower()
            logging.info(f"User selected command: {choice}")
            if choice == 'load':
                cls.load_and_display_history()
            elif choice == 'clear':
                cls.clear_history()
                print("Calculation history cleared.")
            elif choice == 'delete':
                cls.load_and_display_history()
                try:
                    index = int(input("Enter the record number to delete: "))
                    cls.delete_calculation(index)
                    print(f"Calculation at index {index} deleted.")
                except ValueError:
                    print("Invalid input. Please enter a valid number.")
                    logging.warning("User entered invalid number for deletion.")
            elif choice == 'back':
                print("You are in the main menu")
                logging.info("Returning to the main menu.")
                break
            else:
                print("Invalid command. Please enter 'load', 'clear', 'delete', or 'back'.")
                logging.warning("Invalid command entered.")

    @classmethod
    def load_and_display_history(cls):
        cls.load_existing_history()
        if not cls.calculation_history:
            print("No calculations found.")
            logging.info("No calculations found in the history.")
            return

        cls.print_calculation_history()

    @classmethod
    def print_calculation_history(cls):
        """Print the current calculation history."""
        print("Calculation History from CSV:")
        for index, record in enumerate(cls.calculation_history):
            calc_info = f"{record['operation']}: {record['num1']}, {record['num2']}, {record['result']}"
            print(f"{index}: {calc_info}")
            logging.info(f"Record {index}: {calc_info}")
