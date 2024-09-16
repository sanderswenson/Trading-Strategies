from abc import ABC, abstractmethod

class IndicatorBase(ABC):
    @abstractmethod
    def calculate(self, data):
        pass

class SimpleMovingAverage(IndicatorBase):
    def __init__(self, window):
        self.window = window

    def calculate(self, data):
        import logging

        if len(data) < self.window:
            logging.warning(f"Data length ({len(data)}) is less than window size ({self.window}). Returning all None values.")
            return [None] * len(data)
        
        moving_averages = []
        for i in range(len(data)):
            if i < self.window - 1:
                logging.debug(f"Index {i} is less than window size - 1. Appending None.")
                moving_averages.append(None)
            else:
                window_slice = data[i - self.window + 1 : i + 1]
                window_prices = [d['price'] for d in window_slice]
                average = sum(window_prices) / self.window
                moving_averages.append(average)
        
        logging.info(f"Calculated {len(moving_averages)} moving averages, with {moving_averages.count(None)} None values.")
        return moving_averages