import sys
from pathlib import Path
import numpy as np
import pandas as pd
import logging

# Set up logging configuration (adjust the level as needed)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Adding the project root directory to the Python path
project_root = Path(__file__).resolve().parent
sys.path.append(str(project_root))

from data.data_handler import DataHandler
from strategies.strategy_base import MovingAverageCrossover
from strategies.balancer import optimize_scipy
from simulation.simulator1 import simulate_trades

def main():
    data_handler = DataHandler()
    asset_files = ['BCHAIN-MKPRU.csv', 'LBMA-GOLD.csv']
    asset_names = ['BTC', 'GOLD']
    data_dict = {
        name: data_handler.load_csv(filename)
        for name, filename in zip(asset_names, asset_files)
    }
    commission_fees = {'BTC': 0.02, 'GOLD': 0.01}

    # Asset prices in combined df
    btc_df = data_dict.get('BTC').drop(['asset'],axis=1).rename(columns={'price': 'BTC'})
    gold_df = data_dict.get('GOLD').drop(['asset'],axis=1).rename(columns={'price': 'GOLD'})
    all_assets_df = pd.concat([btc_df,gold_df],axis=1).ffill().bfill()

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

    # Signals as combined df
    btc_sig = signals_dict['BTC'].drop(['price','short_ma','long_ma'],axis=1).rename(columns={'signal': 'BTC'})
    gold_sig = signals_dict['GOLD'].drop(['price','short_ma','long_ma'],axis=1).rename(columns={'signal': 'GOLD'})
    signals_df = pd.concat([btc_sig,gold_sig],axis=1)

    # Weights as dict
    weights = {'BTC': 0.97, 'GOLD': 0.03}
    weights_df = pd.DataFrame(index=all_assets_df.index, columns=['Weights'])
    weights_df.at['2016-09-11','Weights'] = weights
    weights_df.at['2016-09-12','Weights'] = weights
    weights_df.at['2016-09-13','Weights'] = weights

    for date in all_assets_df.drop(['2016-09-11', '2016-09-12', '2016-09-13'], axis=0).index:
        date_index = all_assets_df.index.get_loc(date)
        start_index = max(0, date_index - 5)
        period_df = all_assets_df.iloc[start_index:date_index]
        period_returns = period_df.pct_change().dropna()

        if period_returns.empty:
            print(f"Skipping date {date} due to insufficient data.")
            continue

        m = period_returns.mean()
        Q = period_returns.cov()

        # print(f"Mean returns (m) for {date}: {m}")
        # print(f"Covariance matrix (Q) for {date}: {Q}")

        #initial_guess = weights_df.iloc[date_index - 1]['Weights']
        #x0 = np.array([initial_guess['BTC'], initial_guess['GOLD']])
        x0 = np.array([0.97,0.03])


        weights = optimize_scipy(Q, m, x0)
        weights_df.at[date,'Weights'] = {'BTC': weights[0], 'GOLD': weights[1]}

    print(weights_df)


    # Initialize simulator
    # simulator = Simulator(initial_capital=1000, commission_fees=commission_fees)

    # Run simulation
    # trade_history, portfolio_values = simulator.simulate_trades(data_dict, signals_dict)
    portfolio_values = simulate_trades(all_assets_df, weights_df, commission_fees, signals_df, principal=1000)

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
