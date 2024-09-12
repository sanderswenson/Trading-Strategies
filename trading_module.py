class TradingModule:
    def __init__(self, account, risk_percentage=0.3):
        self.account = account
        self.risk_percentage = risk_percentage

    def execute_trade(self, asset, signal, price):
        if signal == 'BUY':
            max_quantity = self.account.cash_balance * self.risk_percentage / price
            if max_quantity > 0:
                quantity = max(0.001, max_quantity)  # Ensure a minimum purchase of 0.001 BTC
                if self.account.buy(asset, quantity, price):
                    print(f"Bought {quantity:.3f} units of {asset} at {price}")
        elif signal == 'SELL':
            quantity = self.account.btc_owned if asset == 'BTC' else self.account.gold_owned
            if quantity > 0:
                if self.account.sell(asset, quantity, price):
                    print(f"Sold {quantity:.3f} units of {asset} at {price}")

