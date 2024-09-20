import pandas as pd
import logging

# Set up logging configuration (adjust the level as needed)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Simulator:
    def __init__(self, initial_capital=1000, commission_fees=None):
        self.initial_capital = initial_capital
        self.commission_fees = commission_fees or {}
        self.cash = initial_capital
        # Positions for each asset
        self.positions = {}
        self.trade_history = []
        self.portfolio_values = []

    def simulate_trades(self, data_dict, signals_dict):
        # Get the union of all dates from all assets
        all_dates = sorted(set().union(*(data.index for data in data_dict.values())))

        for date in all_dates:
            daily_portfolio_value = self.cash
            logging.info(f"Processing date: {date.date()}")

            for asset in data_dict.keys():
                data = data_dict[asset]
                signals = signals_dict[asset]
                commission_fee = self.commission_fees.get(asset, 0)
                position = self.positions.get(asset, 0)

                # Check if price data is available for the asset on this date
                if date in data.index and pd.notna(data.loc[date, 'price']):
                    price = data.loc[date, 'price']

                    # Update daily portfolio value with current holdings
                    daily_portfolio_value += position * price

                    # Check if there's a signal for the asset on this date
                    if date in signals.index:
                        signal_row = signals.loc[date]
                        position_change = signal_row['position']

                        logging.debug(f"Asset: {asset} | Signal: {signal_row['signal']} | Position Change: {position_change} | Price: {price}")

                        # Buy
                        if position_change > 0:
                            units_to_buy = position_change  # This could be a fractional number
                            max_affordable_units = self.cash / (price * (1 + commission_fee))
                            units_to_buy = min(units_to_buy, max_affordable_units)
                            trade_cost = units_to_buy * price * (1 + commission_fee)

                            if units_to_buy > 0:
                                self.cash -= trade_cost
                                self.positions[asset] = position + units_to_buy

                                trade = pd.DataFrame({
                                    'date': [date],
                                    'asset': [asset],
                                    'action': ['buy'],
                                    'units': [units_to_buy],
                                    'price': [price],
                                    'trade_cost': [trade_cost],
                                    'cash': [self.cash],
                                    'position': [self.positions[asset]]
                                })
                                self.trade_history.append(trade)
                                logging.info(f"Executed buy trade: {trade.to_dict('records')[0]}")
                            else:
                                logging.warning(f"Insufficient cash to buy {asset} on {date.date()}. Required: {trade_cost}, Available: {self.cash}")

                        # Sell
                        elif position_change < 0:
                            units_to_sell = min(-position_change, self.positions.get(asset, 0))
                            revenue = units_to_sell * price * (1 - commission_fee)

                            if units_to_sell > 0:
                                self.cash += revenue
                                self.positions[asset] = position - units_to_sell

                                trade = pd.DataFrame({
                                    'date': [date],
                                    'asset': [asset],
                                    'action': ['sell'],
                                    'units': [units_to_sell],
                                    'price': [price],
                                    'revenue': [revenue],
                                    'cash': [self.cash],
                                    'position': [self.positions[asset]]
                                })
                                self.trade_history.append(trade)
                                logging.info(f"Executed sell trade: {trade.to_dict('records')[0]}")
                            else:
                                logging.warning(f"Insufficient units to sell {asset} on {date.date()}. Required: {units_to_sell}, Available: {self.positions.get(asset, 0)}")

                        # No action for position_change == 0

                else:
                    # Price data is missing for this asset on this date
                    logging.warning(f"Price data missing for {asset} on {date.date()}. Skipping trades for this asset today.")

            # Record portfolio value for the day
            self.portfolio_values.append({'date': date, 'portfolio_value': daily_portfolio_value})

        # Convert portfolio values to DataFrame
        portfolio_values_df = pd.DataFrame(self.portfolio_values).set_index('date')

        return self.trade_history, portfolio_values_df
    

# make a function to trade based on target portfolio weights
