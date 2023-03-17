import backtrader as bt
class VWAP(bt.Indicator):
    lines = ('vwap',)
    params = (('period', 30),)
    plotinfo = dict(subplot=False)
    
    def __init__(self):
        self.cumulative_volume = 0.0
        self.cumulative_price_volume = 0.0

    def next(self):
        typical_price = (self.data.high + self.data.low + self.data.close) / 3
        price_volume = typical_price * self.data.volume
        self.cumulative_volume += self.data.volume[0]
        self.cumulative_price_volume += price_volume
        if len(self) >= self.params.period:
            self.lines.vwap[0] = self.cumulative_price_volume / self.cumulative_volume
