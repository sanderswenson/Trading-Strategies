import csv
import pandas as pd
import numpy as np
from datetime import datetime
from pathlib import Path
from contextlib import contextmanager


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
        
        # Handle missing or zero values in 'price'
        df['price'].replace(0, np.nan, inplace=True)   # Replace zeros with NaN
        df['price'].fillna(method='ffill', inplace=True)  # Forward-fill NaN values
        df.dropna(subset=['price'], inplace=True)  # Ensure no remaining NaN values

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

    def save_results(self, portfolio_values, trade_history, signals_dict, filename):
        # Create a DataFrame for portfolio values
        portfolio_df = pd.DataFrame(portfolio_values, columns=['Date', 'Portfolio Value'])
        portfolio_df.set_index('Date', inplace=True)

        # Create a DataFrame for trade history
        trade_df = pd.DataFrame(trade_history, columns=['Date', 'Asset', 'Action', 'Units', 'Price', 'Cost/Revenue'])
        trade_df.set_index('Date', inplace=True)

        # Create a DataFrame for signals
        signals_df = pd.DataFrame(signals_dict)
        signals_df.set_index('Date', inplace=True)

        # Combine all DataFrames
        combined_df = portfolio_df.join([trade_df, signals_df], how='outer')

        # Sort the combined DataFrame by date
        combined_df.sort_index(inplace=True)

        # Save the combined DataFrame to a CSV file
        output_file = self.data_dir / f'{filename}.csv'
        combined_df.to_csv(output_file)

        print(f"Results saved to {output_file}")
