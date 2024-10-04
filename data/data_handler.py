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
        df.dropna(subset=['price'], inplace=True)  # Remove rows with NaN prices

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

    def save_results(self, portfolio_values, filename):
        # Convert portfolio_values to DataFrame
        portfolio_df = pd.DataFrame(portfolio_values).reset_index()

        # Debug print to check the columns of portfolio_df
        print("portfolio_df columns:", portfolio_df.columns)

        # Expand positions and prices dictionaries into separate columns
        positions_df = portfolio_df['positions'].apply(pd.Series)
        prices_df = portfolio_df['prices'].apply(pd.Series)

        # Handle trades
        trades_expanded = portfolio_df[['date', 'trades']].explode('trades')
        if not trades_expanded['trades'].isnull().all():
            trades_df = pd.json_normalize(trades_expanded['trades']).add_prefix('trade_')
            trades_df['Date'] = trades_expanded['date'].values
        else:
            trades_df = pd.DataFrame(columns=['Date', 'trade_Action', 'trade_Asset'])

        # Debug print to check the columns of trades_df
        print("trades_df columns:", trades_df.columns)

        # Merge all data into a single DataFrame
        result_df = pd.concat([
            portfolio_df[['date', 'portfolio_value', 'cash']],
            positions_df.add_suffix('_position'),
            prices_df.add_suffix('_price')
        ], axis=1)

        # Ensure 'date' column is renamed to 'Date' before merging
        result_df.rename(columns={'date': 'Date'}, inplace=True)

        # Debug print to check the columns of result_df before merging
        print("result_df columns before merge:", result_df.columns)

        # Merge trades into the result DataFrame
        result_df = result_df.merge(trades_df, on='Date', how='left')

        # Rename columns to match the desired format
        result_df.rename(columns={
            'portfolio_value': 'Total Portfolio Value',
            'cash': 'Cash',
            'BTC_position': 'BTC',
            'BTC_price': 'BTC Price',
            'GOLD_position': 'Gold',
            'GOLD_price': 'Gold Price'
        }, inplace=True)

        # Select only the required columns
        result_df = result_df[[
            'Date', 'Total Portfolio Value', 'Cash',
            'BTC', 'BTC Price',
            'Gold', 'Gold Price',
        ]]

        # Sort the DataFrame by Date
        result_df.sort_values('Date', inplace=True)

        # Save the DataFrame to a CSV file
        output_file = self.data_dir / f'{filename}.csv'
        result_df.to_csv(output_file, index=False)

        print(f"Results saved to {output_file}")