import backtrader as bt

class MMI(bt.Indicator):
    lines = ('mmi',)
    params = (('period', 14),)

    def __init__(self):
        self.addminperiod(self.params.period)
        self.range = self.data.high - self.data.low
        self.vol = self.data.volume

    def next(self):
        vol_sum = 0
        range_sum = 0
        for i in range(self.params.period):
            vol_sum += self.vol[-i]
            range_sum += self.range[-i]

        mmi_value = 100 * vol_sum / range_sum
        self.lines.mmi[0] = mmi_value