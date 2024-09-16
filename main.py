import sys
from pathlib import Path
import pandas as pd

# Add the project root directory to the Python path
project_root = Path(__file__).resolve().parent
sys.path.append(str(project_root))

from data.data_handler import DataHandler
from strategies.strategy_base import MovingAverageCrossover
from simulation.simulator import Simulator
from utils.performance_evaluator import PerformanceEvaluator

def main():
    data_handler = DataHandler()
    assets = ['BCHAIN-MKPRU.csv', 'LBMA-GOLD.csv']
    data_dict = {asset: data_handler.load_csv(asset) for asset in assets}
    commission_fees = {'BTC': 0.02, 'GOLD': 0.01}

    # Initialize strategies for each asset
    strategies = {
        'BTC': MovingAverageCrossover(short_window=10, long_window=30),
        'GOLD': MovingAverageCrossover(short_window=10, long_window=30)
    }

    # Generate signals for each asset
    signals_dict = {
        asset_key: strategy.generate_signals(data)
        for asset_key, (data, strategy) in zip(data_dict.keys(), zip(data_dict.values(), strategies.values()))
    }

    # Initialize simulator with commission fees as percentages for each asset
    commission_fees = {'BTC': 0.02, 'GOLD': 0.01}  # 2% for BTC, 1% for GOLD
    simulator = Simulator(data_handler, strategies, initial_capital=1000, commission_fees=commission_fees)
    trade_history, portfolio_value = simulator.simulate_trades(data_dict, signals_dict)

    # 3. Run backtest
    # 4. Evaluate performance
    # 5. Display results

if __name__ == "__main__":
    main()