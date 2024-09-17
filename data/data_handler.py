import csv
import pandas as pd
from datetime import datetime
from pathlib import Path


# DataHandler class is responsible for loading and providing access to financial data from CSV files.
# It supports loading data from a specified directory, preprocesses the data, and stores it as a list of dictionaries.
# The class also provides methods to retrieve data for specific assets and time ranges.
class DataHandler:
    def __init__(self, data_dir='data'):
        self.data_dir = Path(data_dir)
        self.data = {}

    def load_csv(self, filename):
        filepath = self.data_dir / filename
        asset_name = filename.split('.')[0]  # Assume filename is "ASSET.csv"
        
        df = pd.read_csv(
            filepath,
            parse_dates=['Date'],
            date_parser=lambda x: datetime.strptime(x, '%m/%d/%y')
        )
        df.rename(columns={'Date': 'date', 'Value': 'price'}, inplace=True)
        df['asset'] = asset_name
        df.set_index('date', inplace=True)
        df.sort_index(inplace=True)
        self.data[asset_name] = df
        return df

    def get_data(self, asset, start_date=None, end_date=None):
        if asset not in self.data:
            self.load_csv(f"{asset}.csv")
        
        data = self.data[asset]
        if start_date and end_date:
            return [d for d in data if start_date <= d['date'] <= end_date]
        return data
    

    def preprocess_data(self, data):
        # Pseudo-code
        # 1. Handle missing values
        # 2. Convert date strings to datetime objects
        # 3. Sort data by date
        # 4. Return preprocessed data
        pass