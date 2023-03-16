# # # # # # # # # # 
# Only 5 days data required
# # # # # # # # # # 

import backtrader as bt
# from shortlisting.main  import shortlisted_stocks

class InsideDayStrategy(bt.Strategy):

    params = (
        ('symbol', True),
        ('shortlisted_stocks', [])
    )

    def __init__(self):
        # self.upper = bt.indicators.BollingerBands(period=5).lines.top
        # self.middle = bt.indicators.BollingerBands(period=5).lines.mid
        # self.lower = bt.indicators.BollingerBands(period=5).lines.bot
        # self.rsi = bt.indicators.RSI(period=14)
        pass
        # self.is_inside_day = False
        
    def next(self):
        pass

    
    def stop(self):
        if (self.data.high[0] <= self.data.high[-2] and self.data.high[-1] <= self.data.high[-2] and \
            self.data.low[0] >= self.data.low[-2] and self.data.low[-1] >= self.data.low[-2]):
        # if (self.data.high[0-1] <= self.data.high[-2-1] and self.data.high[-1-1] <= self.data.high[-2-1] and \
        #     self.data.low[0-1] >= self.data.low[-2-1] and self.data.low[-1-1] >= self.data.low[-2-1]):
            #  (self.data.high[0-1] <= self.data.high[-2-1] and self.data.high[-1-1] <= self.data.high[-2-1] and self.data.low[0-1] >= self.data.low[-2-1] and self.data.low[-1-1] >= self.data.low[-2-1]):
            
            # if self.data.low[-1] < self.lower[-1] and self.rsi[-1] < 30 or \
            #     self.data.high[-1] > self.upper[-1] and self.rsi[-1] > 70:
            
            # if self.rsi[0] < 30 or self.rsi[0] > 70:
        # if (self.data.low[0] > self.lower[0] and self.data.low[-1] < self.lower[-1]) or \
        #     (self.data.high[0] < self.upper[0] and self.data.high[-1] > self.upper[-1]):
            self.params.shortlisted_stocks.append([self.params.symbol.split(":")[1] ,self.data.high[0]])

            # if(self.checkFlagPole(self.data)):

    def checkFlagPole(self, data):
        bullish = True
        bearish = True

        for i in range(2,5):
            if(data.close[-i] < data.close[-i-1] and data.close[-i] < data.close[-i-2]):
                bullish = False
            
        for i in range(1,5):
            if(data.close[-i] > data.close[-i-1] and data.close[-i] > data.close[-i-2]):
                bearish = False

        return bullish or bearish