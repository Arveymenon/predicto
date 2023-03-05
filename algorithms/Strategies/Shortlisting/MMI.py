import backtrader as bt
# from shortlisting.main  import shortlisted_stocks

class MMI(bt.Strategy):
    params = (
        ('symbol', True),
        ('shortlisted_stocks', True)
    )
    def __init__(self):
        self.flag = False


    def next(self):
        if self.MMI.mmi[0] > 50:
            self.flag = True

    def stop(self):
        if self.MMI.mmi[0] > 50:
            self.params.shortlisted_stocks.append([self.params.symbol.split(":")[1] ,self.data.high[0]])