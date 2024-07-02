import logging
import os
from app.commands import Command
import pandas as pd

class CsvCommand(Command):
    def __init__(self):
        self.calculation_history = []

    def add_calculation(self, operation, num1, num2, result):
        self.calculation_history.append({
            'operation': operation,
            'num1': num1,
            'num2': num2,
            'result': result
        })

    def execute(self):
        # Ensure the 'data' directory exists and is writable
        data_dir = 'data'
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
            logging.info(f"The directory '{data_dir}' is created")
        elif not os.access(data_dir, os.W_OK):
            logging.error(f"The directory '{data_dir}' is not writable.")
            return
        
        # Example calculation history for demonstration
        self.add_calculation('addition', 2, 4, 6)
        self.add_calculation('division', 3, 0, 'undef')
        # Add more calculations as needed
        
        # Convert list of dictionaries to DataFrame and save to CSV
        df_history = pd.DataFrame(self.calculation_history)
        csv_file_path = os.path.join(data_dir, 'calculation_history.csv')
        try:
            df_history.to_csv(csv_file_path, index=False)
            logging.info(f"Calculation history saved to CSV at '{csv_file_path}'.")
        except Exception as e:
            logging.error(f"Failed to write CSV file: {e}")
            return
        
        # Read the CSV file back into a DataFrame
        try:
            df_read_history = pd.read_csv(csv_file_path)
            logging.info(f"CSV file '{csv_file_path}' read successfully.")
        except Exception as e:
            logging.error(f"Failed to read CSV file: {e}")
            return
        
        # Print and log each calculation nicely
        print("Calculation History from CSV:")
        for index, row in df_read_history.iterrows():
            # First, print and log the complete record for the calculation
            calc_info = f"{row['operation']}: {row['num1']}, {row['num2']}, {row['result']}"
            #print(f"Record {index}: {calc_info}")
            logging.info(f"Record {index}: {calc_info}")
            
            # Then, iterate through each field in the row to print and log
            for field in row.index:
                field_info = f"    {field}: {row[field]}"
                #print(field_info)
                logging.info(f"Index: {index}, {field_info}")