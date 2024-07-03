import logging
import os
from app.commands import Command
import pandas as pd

class CsvCommand(Command):
    def __init__(self):
        self.calculation_history = []
        self.data_dir = 'data'
        self.csv_file_path = os.path.join(self.data_dir, 'calculation_history.csv')
        self.load_existing_history()
        logging.info("CsvCommand initialized.")

    def load_existing_history(self):
        if os.path.exists(self.csv_file_path):
            try:
                df_existing_history = pd.read_csv(self.csv_file_path)
                self.calculation_history = df_existing_history.to_dict('records')
                logging.info(f"Existing calculation history loaded from '{self.csv_file_path}'.")
            except Exception as e:
                logging.error(f"Failed to read existing CSV file: {e}")

    def add_calculation(self, operation, num1, num2, result):
        self.calculation_history.append({
            'operation': operation,
            'num1': num1,
            'num2': num2,
            'result': result
        })
        self.save_to_csv()
        logging.info(f"Calculation added: {operation}({num1}, {num2}) = {result}")

    def save_to_csv(self):
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
            logging.info(f"The directory '{self.data_dir}' is created.")
        elif not os.access(self.data_dir, os.W_OK):
            logging.error(f"The directory '{self.data_dir}' is not writable.")
            return

        df_history = pd.DataFrame(self.calculation_history)
        try:
            df_history.to_csv(self.csv_file_path, index=False)
            logging.info(f"Calculation history saved to CSV at '{self.csv_file_path}'.")
        except Exception as e:
            logging.error(f"Failed to write CSV file: {e}")

    def clear_history(self):
        '''Clears the history of calculations'''
        self.calculation_history.clear()
        self.save_to_csv()
        logging.info("Calculation history cleared.")

    def delete_calculation(self, index):
        '''Deletes a calculation by index'''
        if 0 <= index < len(self.calculation_history):
            del self.calculation_history[index]
            self.save_to_csv()
            logging.info(f"Calculation at index {index} deleted.")
        else:
            logging.warning(f"Invalid index {index}. Cannot delete calculation.")

    def execute(self):
        print("CSV Command Menu:\n" + '-' * 120)
        print("load ---- clear ---- delete ---- back")
        print('-' * 120)
        print("Type 'back' to return to the main menu.")
        logging.info("CSV Command Menu displayed.")
        
        while True:
            choice = input("Enter a csv command: ").strip().lower()
            logging.info(f"User selected command: {choice}")
            if choice == 'load':
                self.load_and_display_history()
            elif choice == 'clear':
                self.clear_history()
                print("Calculation history cleared.")
            elif choice == 'delete':
                try:
                    index = int(input("Enter the record number to delete: "))
                    self.delete_calculation(index)
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

    def load_and_display_history(self):
        self.load_existing_history()
        if not self.calculation_history:
            print("No calculations found.")
            logging.info("No calculations found in the history.")
            return

        print("Calculation History from CSV:")
        for index, record in enumerate(self.calculation_history):
            calc_info = f"{record['operation']}: {record['num1']}, {record['num2']}, {record['result']}"
            print(f"{index}: {calc_info}")
            logging.info(f"Record {index}: {calc_info}")
