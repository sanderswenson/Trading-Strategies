from abc import ABC, abstractmethod
import pandas as pd
import numpy as np
import logging

class StrategyBase(ABC):
    @abstractmethod
    def generate_signals(self, data):
        pass

class MovingAverageCrossover(StrategyBase):
    def __init__(self, short_window=10, long_window=30):
        self.short_window = short_window
        self.long_window = long_window
        self.signals = None

    def generate_signals(self, df):
        # Ensure 'date' is the index
        if df.index.name != 'date':
            df.set_index('date', inplace=True)
        
        # Calculate short and long moving averages
        df['short_ma'] = df['price'].rolling(window=self.short_window).mean()
        df['long_ma'] = df['price'].rolling(window=self.long_window).mean()

        # Generate signals
        df['signal'] = 0  # Hold
        df.loc[df['short_ma'] > df['long_ma'], 'signal'] = 1  # Buy
        df.loc[df['short_ma'] < df['long_ma'], 'signal'] = -1  # Sell

        # Calculate position changes
        df['position'] = df['signal'].diff().fillna(0)

        # Log the first few signals and positions
        logging.info(f"Signals and positions for the first few entries in the strategy:")
        logging.info(df[['price', 'short_ma', 'long_ma', 'signal', 'position']].head(15))

        self.signals = df[['price', 'short_ma', 'long_ma', 'signal', 'position']].dropna()
        return self.signals