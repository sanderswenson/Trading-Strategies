import sys
from pathlib import Path
import pandas as pd
import logging

# Set up logging configuration (adjust the level as needed)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Adding the project root directory to the Python path
project_root = Path(__file__).resolve().parent
sys.path.append(str(project_root))

from data.data_handler import DataHandler
from strategies.strategy_base import MovingAverageCrossover
from simulation.simulator import Simulator

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

    # Generate signals for each asset
    signals_dict = {}
    for asset in asset_names:
        data = data_dict[asset]
        strategy = strategies[asset]
        signals = strategy.generate_signals(data)
        signals_dict[asset] = signals

    # Verify that signals are generating trades
    for asset in asset_names:
        signals = signals_dict[asset]
        print(f"Signals for {asset}:\n", signals[['price', 'short_ma', 'long_ma', 'signal']])

    # Initialize simulator
    simulator = Simulator(initial_capital=1000, commission_fees=commission_fees)

    # Run simulation
    trade_history, portfolio_values = simulator.simulate_trades(data_dict, signals_dict)

    # Print trade history
    #print("\nTrade History:")
    #print(trade_history)

    # Print portfolio value over time
    print("\nPortfolio Value Over Time:")
    print(portfolio_values)

    # Prompt for file name and save results if provided
    filename = input("Enter a filename to save results (leave blank to skip saving): ").strip()
    if filename:
        data_handler.save_results(portfolio_values, filename)
    else:
        print("Results not saved.")

if __name__ == "__main__":
    main()