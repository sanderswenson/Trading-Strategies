from abc import ABC, abstractmethod
import pandas as pd

class IndicatorBase(ABC):
    @abstractmethod
    def calculate(self, data):
        pass

class SimpleMovingAverage(IndicatorBase):
    def __init__(self, window):
        self.window = window

    def calculate(self, df):
        if df.index.name != 'date':
            df.set_index('date', inplace=True)
        df['sma'] = df['price'].rolling(window=self.window).mean()
        return df['sma']