class TradingModule:
    def __init__(self, account, risk_percentage=1):
        self.account = account
        self.risk_percentage = risk_percentage

    def execute_trade(self, signal, price):
        if signal == 'BUY':
            max_quantity = int(self.account.cash_balance * self.risk_percentage / price)
            if max_quantity > 0:
                self.account.buy(max_quantity, price)
                print(f"Bought {max_quantity} units at {price}")
        elif signal == 'SELL':
            quantity = self.account.owned_assets
            if quantity > 0:
                self.account.sell(quantity, price)
                print(f"Sold {quantity} units at {price}")

