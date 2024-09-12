class AccountBalanceTracker:
    def __init__(self, initial_balance):
        self.cash_balance = initial_balance
        self.btc_owned = 0
        self.btc_price = 0
        self.gold_owned = 0
        self.gold_price = 0

    def buy(self, asset, quantity, price):
        if asset == 'BTC':
            commission = 0.02
        elif asset == 'Gold':
            commission = 0.01
        else:
            return False

        cost = quantity * price * (1 + commission)
        if cost <= self.cash_balance:
            self.cash_balance -= cost
            if asset == 'BTC':
                self.btc_owned += quantity
                self.btc_price = price
            elif asset == 'Gold':
                self.gold_owned += quantity
                self.gold_price = price
            return True
        return False

    def sell(self, asset, quantity, price):
        if asset == 'BTC':
            commission = 0.02
            if quantity <= self.btc_owned:
                self.cash_balance += quantity * price * (1 - commission)
                self.btc_owned -= quantity
                if self.btc_owned == 0:
                    self.btc_price = 0
                return True
        elif asset == 'Gold':
            commission = 0.01
            if quantity <= self.gold_owned:
                self.cash_balance += quantity * price * (1 - commission)
                self.gold_owned -= quantity
                if self.gold_owned == 0:
                    self.gold_price = 0
                return True
        return False

    def get_total_value(self, btc_price, gold_price):
        return self.cash_balance + (self.btc_owned * btc_price) + (self.gold_owned * gold_price)