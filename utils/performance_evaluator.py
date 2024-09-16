import numpy as np
from abc import ABC, abstractmethod

class PerformanceEvaluator(ABC):
    @abstractmethod
    def evaluate(self, portfolio_values):
        pass

class ReturnsEvaluator(PerformanceEvaluator):
    def evaluate(self, portfolio_values):
        # Calculate daily returns
        pass

class SharpeRatioEvaluator(PerformanceEvaluator):
    def __init__(self, risk_free_rate=0.02):
        self.risk_free_rate = risk_free_rate

    def evaluate(self, portfolio_values):
        # Calculate Sharpe ratio
        pass

class MaxDrawdownEvaluator(PerformanceEvaluator):
    def evaluate(self, portfolio_values):
        # Calculate maximum drawdown
        pass