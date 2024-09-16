from abc import ABC, abstractmethod
import pandas as pd
import numpy as np

class StrategyBase(ABC):
    @abstractmethod
    def generate_signals(self, data):
        pass

class MovingAverageCrossover(StrategyBase):
    def __init__(self, short_window=10, long_window=30):
        self.short_window = short_window
        self.long_window = long_window
        self.signals = None

    def generate_signals(self, data):
        # Convert list of dicts to DataFrame
        df = pd.DataFrame(data)
        df.set_index('date', inplace=True)
        
        # Calculate short and long moving averages
        df['short_ma'] = df['price'].rolling(window=self.short_window).mean()
        df['long_ma'] = df['price'].rolling(window=self.long_window).mean()

        # Generate buy/sell signals
        df['signal'] = 0  # Initialize signal column with 0 (hold)
        df.loc[df['short_ma'] > df['long_ma'], 'signal'] = 1  # Buy signal
        df.loc[df['short_ma'] < df['long_ma'], 'signal'] = -1  # Sell signal

        # Generate trading signals
        df['position'] = df['signal'].diff()

        # Store signals
        self.signals = df[['price', 'short_ma', 'long_ma', 'signal', 'position']].dropna()

        return self.signals