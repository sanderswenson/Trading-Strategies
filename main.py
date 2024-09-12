from data_loader import DataLoader
from analysis_framework import SMA_Momentum
from account_balance_tracker import AccountBalanceTracker
from trading_module import TradingModule
import os
import csv

def main():
    # Load data
    data = DataLoader.load_csv('BCHAIN-MKPRU.csv')
    print(f"Loaded {len(data)} data points")

    # Initialize account and trading module
    account = AccountBalanceTracker(initial_balance=1000)
    trading_module = TradingModule(account)

    # Generate signals
    signals = SMA_Momentum.generate_signals(data)
    print(f"Generated {len(signals)} signals")

    # Prompt for a name
    output_name = input("Enter a name for the output (leave blank for console output): ").strip()

    # Simulate trading
    results = []
    for i, (signal, date, price) in enumerate(signals):
        trading_module.execute_trade('BTC', signal, price)
        
        result = {
            "Date": date,
            "Signal": signal,
            "Price": price,
            "Cash": account.cash_balance,
            "BTC": account.btc_owned,
            "Total Value": account.get_total_value(price, 0)
        }
        results.append(result)
        
        # Print every 10th iteration to reduce output (only if output_name is blank)
        if not output_name and i % 10 == 0:
            print(f"Date: {date}, Signal: {signal}, Price: {price:.2f}, "
                  f"Cash: {account.cash_balance:.2f}, BTC: {account.btc_owned}, "
                  f"Total Value: {account.get_total_value(price, 0):.2f}")

    # Output results
    if output_name:
        # Generate CSV in /Tests/ directory
        os.makedirs("Tests", exist_ok=True)
        csv_path = os.path.join("Tests", f"{output_name}.csv")
        with open(csv_path, 'w', newline='') as csvfile:
            fieldnames = ["Date", "Signal", "Price", "Cash", "BTC", "Total Value"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for row in results:
                writer.writerow(row)
        print(f"Results saved to {csv_path}")
    else:
        # Print final results to console
        print("\nFinal Results:")
        print(f"Cash: {account.cash_balance:.2f}")
        print(f"BTC owned: {account.btc_owned}")
        print(f"Total Value: {account.get_total_value(price, 0):.2f}")

if __name__ == "__main__":
    main()