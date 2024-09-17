import pandas as pd

class Simulator:
    def __init__(self, data_handler, strategies, initial_capital=1000, commission_fees=None):
        self.data_handler = data_handler
        self.strategies = strategies  # Dictionary of strategies for each asset
        self.initial_capital = initial_capital
        # Commission fees per asset as a percentage (e.g., {'BTC': 0.02, 'GOLD': 0.01})
        self.commission_fees = commission_fees or {}

    def simulate_trades(self, data_dict, signals_dict):
        # Initialize portfolio with cash and empty holdings
        portfolio = {
            'cash': self.initial_capital,
            'holdings': {asset: 0 for asset in data_dict.keys()}
        }
        trade_history = []
        portfolio_value = []

        # Combine all dates from data and signals
        all_dates = sorted(set(
            date for data in data_dict.values() for date in data.index
        ).union(
            date for signals in signals_dict.values() for date in signals.index
        ))

        # Initialize current prices dict with None
        last_valid_prices = {asset: None for asset in data_dict.keys()}

        for date in all_dates:
            daily_values = {'date': date}
            # Update current prices, using the last valid price if current is missing
            current_prices = {}
            for asset, data in data_dict.items():
                if date in data.index and pd.notna(data.loc[date]['price']):
                    current_price = data.loc[date]['price']
                    last_valid_prices[asset] = current_price  # Update last valid price
                else:
                    current_price = last_valid_prices[asset]  # Use last valid price
                current_prices[asset] = current_price

            # Process signals for each asset
            for asset, signals in signals_dict.items():
                if date in signals.index:
                    position = signals.loc[date]['position']
                    current_price = current_prices.get(asset)

                    if pd.notna(current_price):  # Check if there's a valid price
                        if position == 1:  # Buy signal
                            self.execute_trade(
                                portfolio, asset, current_price, 'buy', date, trade_history
                            )
                        elif position == -1:  # Sell signal
                            self.execute_trade(
                                portfolio, asset, current_price, 'sell', date, trade_history
                            )

            # Calculate total portfolio value
            total_asset_value = sum(
                portfolio['holdings'][asset] * (current_prices.get(asset) or 0)
                for asset in portfolio['holdings']
            )
            total_value = portfolio['cash'] + total_asset_value
            daily_values['value'] = total_value
            portfolio_value.append(daily_values)

        return trade_history, portfolio_value

    def execute_trade(self, portfolio, asset, price, action, date, trade_history):
        commission_rate = self.commission_fees.get(asset, 0)
        allocation = self.get_asset_allocation(asset)

        if action == 'buy':
            invest_amount = portfolio['cash'] * allocation
            # Adjust the price to include commission
            adjusted_price = price * (1 + commission_rate)
            shares_to_buy = invest_amount // adjusted_price
            total_cost = shares_to_buy * adjusted_price
            if shares_to_buy > 0 and total_cost <= portfolio['cash']:
                portfolio['cash'] -= total_cost
                portfolio['holdings'][asset] += shares_to_buy
                trade_history.append({
                    'date': date,
                    'asset': asset,
                    'action': 'buy',
                    'price': price,
                    'shares': shares_to_buy,
                    'cost': total_cost,
                    'commission': total_cost - (shares_to_buy * price)
                })
        elif action == 'sell':
            shares_to_sell = portfolio['holdings'][asset]
            if shares_to_sell > 0:
                # Adjust the price to include commission
                adjusted_price = price * (1 - commission_rate)
                revenue = shares_to_sell * adjusted_price
                portfolio['cash'] += revenue
                portfolio['holdings'][asset] = 0
                trade_history.append({
                    'date': date,
                    'asset': asset,
                    'action': 'sell',
                    'price': price,
                    'shares': shares_to_sell,
                    'revenue': revenue,
                    'commission': (shares_to_sell * price) - revenue
                })

    def get_asset_allocation(self, asset):
        # Define target allocation for each asset
        target_allocations = {
            'BTC': 0.5,   # 50% allocation
            'GOLD': 0.5   # 50% allocation
            # Add more assets and their target allocations as needed
        }
        return target_allocations.get(asset, 0)