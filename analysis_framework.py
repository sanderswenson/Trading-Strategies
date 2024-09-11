class AnalysisFramework:
    @staticmethod
    def simple_moving_average(data, window):
        if len(data) < window:
            return None
        return sum(price['price'] for price in data[-window:]) / window

    @staticmethod
    def generate_signals(data, sma_short=10, sma_long=30):
        signals = []
        for i in range(len(data)):
            if i >= sma_long - 1:
                short_sma = AnalysisFramework.simple_moving_average(data[i-sma_short+1:i+1], sma_short)
                long_sma = AnalysisFramework.simple_moving_average(data[i-sma_long+1:i+1], sma_long)
                if short_sma > long_sma:
                    signals.append(('BUY', data[i]['date'], data[i]['price']))
                elif short_sma < long_sma:
                    signals.append(('SELL', data[i]['date'], data[i]['price']))
                else:
                    signals.append(('HOLD', data[i]['date'], data[i]['price']))
            else:
                signals.append(('HOLD', data[i]['date'], data[i]['price']))
        return signals