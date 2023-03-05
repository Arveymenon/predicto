import backtrader as bt
from shortlisting.main  import shortlisted_stocks

class BBRSIStrategy(bt.Strategy):

    params = (
        ('symbol', True),
        ('temp', True)
    )
    
    def __init__(self):
        self.upper = bt.indicators.BollingerBands(period=20).lines.top
        self.middle = bt.indicators.BollingerBands(period=20).lines.mid
        self.lower = bt.indicators.BollingerBands(period=20).lines.bot
        self.rsi = bt.indicators.RSI(period=14)

    def next(self):
        # # Buy signal
        # if self.data.close[-1] < self.lower[-1] and self.rsi[-1] < 30:
        #     self.buy()

        # # Sell signal
        # if self.data.close[-1] > self.upper[-1] and self.rsi[-1] > 70:
        #     self.sell()
        pass

    def stop(self):
        if self.data.close[-1] < self.lower[-1] and self.rsi[-1] < 30 or \
            self.data.close[-1] > self.upper[-1] and self.rsi[-1] > 70:

            shortlisted_stocks.append([self.params.symbol.split(":")[1] ,self.data.high[0]])