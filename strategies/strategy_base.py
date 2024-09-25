from abc import ABC, abstractmethod
import pandas as pd
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
        if df.index.name != 'date':
            df = df.set_index('date')

        # Handle missing price data by dropping rows with NaN in 'price'
        df = df.dropna(subset=['price'])

        # Calculate moving averages
        df['short_ma'] = df['price'].rolling(window=self.short_window, min_periods=1).mean()
        df['long_ma'] = df['price'].rolling(window=self.long_window, min_periods=1).mean()

        # Generate signals: Buy (1), Sell (-1), Hold (0)
        df['signal'] = 0
        df.loc[df['short_ma'] > df['long_ma'], 'signal'] = 1
        df.loc[df['short_ma'] < df['long_ma'], 'signal'] = -1

        # Log signals for debugging
        logging.debug(f"Generated signals:\n{df[['price', 'short_ma', 'long_ma', 'signal']].head()}")

        self.signals = df[['price', 'short_ma', 'long_ma', 'signal']].copy()
        return self.signals