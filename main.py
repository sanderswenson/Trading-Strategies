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
    asset_files = ['BCHAIN-MKPRU.csv', 'LBMA-GOLD.csv']
    asset_names = ['BTC', 'GOLD']
    data_dict = {
        name: data_handler.load_csv(filename)
        for name, filename in zip(asset_names, asset_files)
    }
    commission_fees = {'BTC': 0.02, 'GOLD': 0.01}

    # Initialize strategies
    strategies = {
        'BTC': MovingAverageCrossover(short_window=10, long_window=30),
        'GOLD': MovingAverageCrossover(short_window=10, long_window=30)
    }

    # Generate signals
    signals_dict = {
        name: strategies[name].generate_signals(data)
        for name, data in data_dict.items()
    }

    # Initialize simulator
    commission_fees = {'BTC': 0.02, 'GOLD': 0.01}  # 2% for BTC, 1% for GOLD
    simulator = Simulator(
        data_handler, strategies,
        initial_capital=1000, commission_fees=commission_fees
    )
    trade_history, portfolio_value = simulator.simulate_trades(data_dict, signals_dict)
    
    # Print a few trade signals for each asset
    for asset, signals in signals_dict.items():
        print(f"\nTrade signals for {asset}:")
        pd.set_option('display.max_rows', None)
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', None)
        print(signals[['price', 'signal', 'position']].head(30))
        pd.reset_option('display.max_rows')
        pd.reset_option('display.max_columns')
        pd.reset_option('display.width')
    # Print portfolio value
    print("\nFinal portfolio value:")
    print(portfolio_value)

if __name__ == "__main__":
    main()