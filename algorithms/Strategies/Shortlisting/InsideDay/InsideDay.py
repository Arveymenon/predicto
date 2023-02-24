# # # # # # # # # # 
# Only 5 days data required
# # # # # # # # # # 

import backtrader as bt
from shortlisting.shortlisting  import shortlisted_stocks

class InsideDayStrategy(bt.Strategy):

    params = (
        ('symbol', True),
        ('temp', True)
    )

    def __init__(self):
        self.is_inside_day = False
        
    def next(self):

        print("------------")
        print(self.params.symbol)
        print(self.data.high[0], self.data.high[-1], self.data.high[-2])
        print(self.data.low[0], self.data.low[-1], self.data.low[-2])
        print("------------")

    
    def stop(self):
        if self.data.high[0] <= self.data.high[-2] and self.data.high[-1] <= self.data.high[-2] and \
                self.data.low[0] >= self.data.low[-2] and self.data.low[-1] >= self.data.low[-2]:
            self.is_inside_day = True
            shortlisted_stocks.append(self.params.symbol)
        else:
            self.is_inside_day = False