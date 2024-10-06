import numpy  as np
import pandas as pd

def simulate_trades(all_assets_df, weights, commissions, signals_df, principal=1000):

    # TODO: make cash an asset? doesn't seem standard, but it might make sense.
    portfolio = pd.DataFrame(index=all_assets_df.index, columns=all_assets_df.columns)
    portfolio[:] = 0
    cash = principal

    portfolio_value = pd.DataFrame(index=all_assets_df.index, columns=["Portfolio Value"])

    # track portfolio
    portfolio_hist = pd.Series(0, index=all_assets_df.columns)

    for date in all_assets_df.index:
        current_prices = all_assets_df.loc[date]
        signals = signals_df.loc[date]  # 1 is buy -1 is sell 0 is hold

        if date != all_assets_df.index[0]:
            portfolio.loc[date] = portfolio_hist

        net_worth = cash + (portfolio.loc[date] * current_prices).sum()
        # putting EVERYTHING on the line
        target_allocation = {asset: weights[asset] * net_worth for asset in all_assets_df.columns}

        # mean returns in past 5 day period
        date_index = all_assets_df.index.get_loc(date)
        start_index = max(0, date_index - 5)
        period_df = all_assets_df.iloc[start_index:date_index]
        mean_returns = period_df.pct_change().mean()

        # actual simulation
        for asset in all_assets_df.columns:
            signal = signals[asset]
            current_position = portfolio.loc[date, asset]
            current_price = current_prices[asset]
            target_value = target_allocation[asset]
            target_units = target_value / current_price

            # TODO: alter expected returns? could be based on more than mean_returns.
            expected_return = mean_returns[asset]

            # consider cost of target allocation
            if target_units > current_position:
                units_to_buy = target_units - current_position
                trade_value = units_to_buy * current_price
                commission_cost = trade_value * commissions[asset]

                # expected gain from HOLDING target position
                expected_gain = trade_value * expected_return

                # only trades if expected gain exceeds commission cost
                # TODO: should we add more criteria?
                if signal == 1 and expected_gain > commission_cost and cash >= trade_value + commission_cost:
                    portfolio.loc[date, asset] += units_to_buy
                    cash -= trade_value + commission_cost

            elif target_units < current_position:
                units_to_sell = current_position - target_units
                trade_value = units_to_sell * current_price
                commission_cost = trade_value * commissions[asset]

                # expected loss from SELLING (selling reduces exposure to expected gain)
                expected_loss = trade_value * expected_return

                if signal == -1 and expected_loss > commission_cost:
                    portfolio.loc[date, asset] -= units_to_sell
                    cash += trade_value - commission_cost

        # update previous_portfolio
        portfolio_hist = portfolio.loc[date]

        # data outputs
        total_portfolio_value = cash + (portfolio.loc[date] * current_prices).sum()
        portfolio_value.loc[date, "Portfolio Value"] = total_portfolio_value

    return portfolio_value
