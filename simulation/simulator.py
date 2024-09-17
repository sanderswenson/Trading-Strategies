import pandas as pd
import logging

# Set up logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Simulator:
    def __init__(self, data_handler, strategies, initial_capital=1000, commission_fees=None):
        self.data_handler = data_handler
        self.strategies = strategies
        self.initial_capital = initial_capital
        self.commission_fees = commission_fees if commission_fees else {}
        self.positions = {asset: 0 for asset in strategies.keys()}
        self.trade_history = []

    def simulate_trades(self, data_dict, signals_dict):
        # Initialize portfolio value history
        portfolio_values = []

        # Corrected: Combine all dates from signals
        all_dates = sorted(set().union(*[signals.index for signals in signals_dict.values()]))

        for date in all_dates:
            for asset, signals in signals_dict.items():
                if date in signals.index:
                    signal_row = signals.loc[date]
                    position_change = signal_row['position']
                    price = signal_row['price']
                    fee_rate = self.commission_fees.get(asset, 0)

                    # Log the signal and position change
                    logging.debug(f"Asset: {asset} | Signal: {signal_row['signal']} | Position Change: {position_change} | Price: {price}")

                    # Buy
                    if position_change > 0:
                        # Calculate total cost including commission
                        trade_cost = position_change * price * (1 + fee_rate)
                        logging.debug(f"Attempting to buy {position_change} units of {asset} at {price} per unit with {fee_rate*100}% fee. Total cost: {trade_cost}")

                        if self.initial_capital >= trade_cost:
                            # Update positions and capital
                            self.positions[asset] += position_change
                            self.initial_capital -= trade_cost

                            # Log the trade execution
                            trade = {
                                'date': date,
                                'asset': asset,
                                'position_change': position_change,
                                'price': price,
                                'trade_amount': trade_cost,
                                'fee': trade_cost - (position_change * price),
                                'capital': self.initial_capital,
                                'positions': self.positions.copy()
                            }
                            logging.info(f"Executed buy trade: {trade}")
                            self.trade_history.append(trade)
                        else:
                            logging.warning(f"Not enough capital to buy {position_change} units of {asset} on {date.date()}. Needed: {trade_cost}, Available: {self.initial_capital}")

                    # Sell
                    elif position_change < 0:
                        sell_units = -position_change
                        if self.positions[asset] >= sell_units:
                            # Calculate net revenue after commission
                            gross_revenue = sell_units * price
                            fee = gross_revenue * fee_rate
                            net_revenue = gross_revenue - fee

                            # Update positions and capital
                            self.positions[asset] -= sell_units
                            self.initial_capital += net_revenue

                            # Log the trade execution
                            trade = {
                                'date': date,
                                'asset': asset,
                                'position_change': -sell_units,
                                'price': price,
                                'trade_amount': net_revenue,
                                'fee': fee,
                                'capital': self.initial_capital,
                                'positions': self.positions.copy()
                            }
                            logging.info(f"Executed sell trade: {trade}")
                            self.trade_history.append(trade)
                        else:
                            logging.warning(f"Not enough {asset} to sell {sell_units} units on {date.date()}. Current position: {self.positions[asset]}")

                    else:
                        # No trade
                        logging.debug(f"No position change for {asset} on {date.date()}")
                else:
                    logging.debug(f"No signal for {asset} on {date.date()}")

            # Calculate total portfolio value for the day
            total_asset_value = sum(
                self.positions[asset] * data_dict[asset].loc[date, 'price']
                if date in data_dict[asset].index else 0
                for asset in self.positions
            )
            portfolio_value = self.initial_capital + total_asset_value
            portfolio_values.append({'date': date, 'portfolio_value': portfolio_value})

            logging.debug(f"Total portfolio value on {date.date()}: {portfolio_value}")

        # Convert portfolio values to DataFrame
        portfolio_values_df = pd.DataFrame(portfolio_values).set_index('date')

        return self.trade_history, portfolio_values_df