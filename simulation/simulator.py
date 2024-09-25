import pandas as pd
import logging

# Set up logging configuration (adjust the level as needed)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Simulator:
    def __init__(self, initial_capital=1000, commission_fees=None):
        self.commission_fees = commission_fees or {}
        self.cash = initial_capital
        # Positions for each asset
        self.positions = {} 
        '''
        I want this to handle all the positions? 
        Maybe doing a fractionals and current assets rather than random
        positional ideas from the strategy base?
        '''
        self.trade_history = []
        self.portfolio_values = []

    def simulate_trades(self, data_dict, signals_dict):
        # Get the union of all dates from all assets
        all_dates = sorted(set().union(*(data.index for data in data_dict.values())))

        for date in all_dates:
            daily_portfolio_value = self.cash

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
                        position_change = signal_row['signal']

                        logging.debug(f"Asset: {asset} | Signal: {signal_row['signal']} | Position Change: {position_change} | Price: {price}")

                        # Execute trades based on the signal
                        self.execute_trade(date, asset, position_change, price, commission_fee)

                else:
                    # Price data is missing for this asset on this date
                    #logging.warning(f"Price data missing for {asset} on {date.date()}. Skipping trades for this asset today.")
                    pass

            # Record portfolio value for the day
            self.portfolio_values.append({'date': date, 'portfolio_value': daily_portfolio_value})

        # Convert portfolio values to DataFrame
        portfolio_values_df = pd.DataFrame(self.portfolio_values).set_index('date')

        return self.trade_history, portfolio_values_df

    def execute_trade(self, date, asset, position_change, price, commission_fee):
        if position_change > 0:
            units_to_buy = position_change  # This could be a fractional number
            max_affordable_units = self.cash / (price * (1 + commission_fee))
            units_to_buy = min(units_to_buy, max_affordable_units)
            trade_cost = units_to_buy * price * (1 + commission_fee)

            if units_to_buy > 0:
                self.cash -= trade_cost
                self.positions[asset] = self.positions.get(asset, 0) + units_to_buy

                trade = {
                    'Date': date,
                    'Asset': asset,
                    'Action': 'buy',
                    'Units': units_to_buy,
                    'Price': price,
                    'Cost/Revenue': trade_cost,
                    'Cash': self.cash,
                    'Position': self.positions[asset]
                }
                self.trade_history.append(trade)
                logging.info(f"Buy: {asset} | Units: {units_to_buy:.4f} | Price: {price:.2f} | Cost: {trade_cost:.2f} | Cash: {self.cash:.2f} | Position: {self.positions[asset]:.4f}")
            else:
                #logging.warning(f"Insufficient cash to buy {asset} on {date}. Required: {trade_cost}, Available: {self.cash}")
                pass

        elif position_change < 0:
            units_to_sell = min(-position_change, self.positions.get(asset, 0))
            revenue = units_to_sell * price * (1 - commission_fee)

            if units_to_sell > 0:
                self.cash += revenue
                self.positions[asset] = self.positions.get(asset, 0) - units_to_sell

                trade = {
                    'Date': date,
                    'Asset': asset,
                    'Action': 'sell',
                    'Units': units_to_sell,
                    'Price': price,
                    'Cost/Revenue': revenue,
                    'Cash': self.cash,
                    'Position': self.positions[asset]
                }
                self.trade_history.append(trade)
                logging.info(f"Sell: {asset} | Units: {units_to_sell:.4f} | Price: {price:.2f} | Revenue: {revenue:.2f} | Cash: {self.cash:.2f} | Position: {self.positions[asset]:.4f}")
            else:
                #logging.warning(f"Insufficient units to sell {asset} on {date}. Required: {units_to_sell}, Available: {self.positions.get(asset, 0)}")
                pass

        # No action for position_change == 0

# make a function to trade based on target portfolio weights