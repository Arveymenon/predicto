import backtrader as bt

class CGPTGeneratedStrategy(bt.Strategy):
    params = (
        ('sma_period', 20),
        ('atr_period', 14),
        ('rsi_period', 14),
        ('rsi_upper', 70),
        ('rsi_lower', 30),
        ('trailing_stop_pct', 0.02),
        ('take_profit_pct', 0.03),
        ('test', True)
    )

    def __init__(self):
        self.sma = bt.indicators.SimpleMovingAverage(
            self.data.close, period=self.params.sma_period)
        self.atr = bt.indicators.ATR(self.data, period=self.params.atr_period)
        self.rsi = bt.indicators.RSI(self.data, period=self.params.rsi_period)
        self.stop_price = 0

    def next(self):
        if self.position.size == 0:
            # Buy signal
            if self.data.close > self.sma and \
               self.rsi < self.params.rsi_lower:
                self.buy(size=1)

        elif self.position.size > 0:
            # Trailing stop
            stop_price = self.data.close * \
                (1 - self.params.trailing_stop_pct)
            if stop_price > self.stop_price:
                self.stop_price = stop_price
            self.sell(exectype=bt.Order.Stop, price=self.stop_price)

            # Take profit
            take_profit_price = self.data.close * \
                (1 + self.params.take_profit_pct)
            self.sell(exectype=bt.Order.Limit, price=take_profit_price)

        # Print some debug information
        print(f"Close: {self.data.close[0]}, SMA: {self.sma[0]}, "
              f"ATR: {self.atr[0]}, RSI: {self.rsi[0]}")