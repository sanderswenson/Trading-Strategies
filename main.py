from data_loader import DataLoader
from analysis_framework import AnalysisFramework
from account_balance_tracker import AccountBalanceTracker
from trading_module import TradingModule

def main():
    # Load data
    data = DataLoader.load_csv('BCHAIN-MKPRU.csv')
    print(f"Loaded {len(data)} data points")

    # Initialize account and trading module
    account = AccountBalanceTracker(initial_balance=1000)
    trading_module = TradingModule(account)

    # Generate signals
    signals = AnalysisFramework.generate_signals(data)
    print(f"Generated {len(signals)} signals")

    # Simulate trading
    for i, (signal, date, price) in enumerate(signals):
        trading_module.execute_trade(signal, price)
        
        # Print every 100th iteration to reduce output
        if i % 100 == 0:
            print(f"Date: {date}, Signal: {signal}, Price: {price:.2f}, "
                  f"Cash: {account.cash_balance:.2f}, Assets: {account.owned_assets}, "
                  f"Total Value: {account.get_total_value(price):.2f}")

    # Print final results
    print("\nFinal Results:")
    print(f"Cash: {account.cash_balance:.2f}")
    print(f"Assets: {account.owned_assets}")
    print(f"Total Value: {account.get_total_value(price):.2f}")

if __name__ == "__main__":
    main()