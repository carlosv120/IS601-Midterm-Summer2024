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

    def save_to_csv(self):
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
            logging.info(f"The directory '{self.data_dir}' is created")
        elif not os.access(self.data_dir, os.W_OK):
            logging.error(f"The directory '{self.data_dir}' is not writable.")
            return

        df_history = pd.DataFrame(self.calculation_history)
        try:
            df_history.to_csv(self.csv_file_path, index=False)
            logging.info(f"Calculation history saved to CSV at '{self.csv_file_path}'.")
        except Exception as e:
            logging.error(f"Failed to write CSV file: {e}")

    def execute(self):
        try:
            df_read_history = pd.read_csv(self.csv_file_path)
            logging.info(f"CSV file '{self.csv_file_path}' read successfully.")
        except Exception as e:
            logging.error(f"Failed to read CSV file: {e}")
            return

        print("Calculation History from CSV:")
        for index, row in df_read_history.iterrows():
            calc_info = f"{row['operation']}: {row['num1']}, {row['num2']}, {row['result']}"
            logging.info(f"Record {index}: {calc_info}")
            for field in row.index:
                field_info = f"    {field}: {row[field]}"
                logging.info(f"Index: {index}, {field_info}")
