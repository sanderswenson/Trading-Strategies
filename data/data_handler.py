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
        # Create DataFrame for portfolio values
        portfolio_df = pd.DataFrame(portfolio_values).reset_index(drop=True)
        portfolio_df.rename(columns={'date': 'Date', 'portfolio_value': 'Portfolio_Value'}, inplace=True)

        # Create DataFrame for trade history
        trade_df = pd.DataFrame(trade_history).reset_index(drop=True)
        trade_df.rename(columns={'Date': 'Trade_Date'}, inplace=True)

        # Process signals_dict to create a combined signals DataFrame
        signals_list = []
        for asset, signals in signals_dict.items():
            temp_df = signals.copy()
            temp_df.reset_index(inplace=True)
            temp_df.rename(columns={
                'date': 'Date',
                'signal': f'{asset}_signal',
                'position': f'{asset}_position'
            }, inplace=True)
            signals_list.append(temp_df)

        # Concatenate all signals DataFrames column-wise
        signals_df = pd.concat(signals_list, axis=1)
        # Remove duplicate 'Date' columns if any
        signals_df = signals_df.loc[:, ~signals_df.columns.duplicated()]

        # Combine all DataFrames column-wise
        combined_df = pd.concat([portfolio_df, trade_df, signals_df], axis=1)

        # Align data with all possible dates
        all_dates = pd.date_range(start=combined_df['Date'].min(), end=combined_df['Date'].max())
        combined_df = combined_df.set_index('Date').reindex(all_dates).reset_index().rename(columns={'index': 'Date'})

        # Align trade_df with all possible dates
        trade_df = trade_df.set_index('Trade_Date').reindex(all_dates).reset_index().rename(columns={'index': 'Trade_Date'})

        # Save the combined DataFrame to a CSV file
        output_file = self.data_dir / f'{filename}.csv'
        combined_df.to_csv(output_file, index=False)

        print(f"Results saved to {output_file}")
