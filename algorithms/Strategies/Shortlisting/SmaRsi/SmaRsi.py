import backtrader as bt
from shortlisting.shortlisting  import shortlisted_stocks

class SMARSI_Strategy(bt.Strategy):
    
    params = (
        ('symbol', True),
        ('rsi_period', 14),
        ('ma_period', 20),
        ('oversold', 30),
        ('overbought', 70),
    )
    
    def __init__(self):
        self.rsi = bt.indicators.RSI(period=self.params.rsi_period)
        self.ma = bt.indicators.SimpleMovingAverage(period=self.params.ma_period)
        
    def next(self):
        pass

    def stop(self):
        if self.rsi < self.params.oversold or self.rsi > self.params.overbought:
            shortlisted_stocks.append(self.params.symbol)
