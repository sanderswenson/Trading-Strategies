class AccountBalanceTracker:
    def __init__(self, initial_balance):
        self.cash_balance = initial_balance
        self.owned_assets = 0
        self.asset_price = 0

    def buy(self, quantity, price):
        cost = quantity * price * 0.98
        if cost <= self.cash_balance:
            self.cash_balance -= cost
            self.owned_assets += quantity
            self.asset_price = price
            return True
        return False

    def sell(self, quantity, price):
        if quantity <= self.owned_assets:
            self.cash_balance += quantity * price * 0.98
            self.owned_assets -= quantity
            if self.owned_assets == 0:
                self.asset_price = 0
            return True
        return False

    def get_total_value(self, current_price):
        return self.cash_balance + (self.owned_assets * current_price)