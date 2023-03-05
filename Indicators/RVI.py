import backtrader as bt

class RVI(bt.Indicator):
    '''
    Relative Vigor Index (RVI) indicator as described by John Ehlers.
    https://www.tradingview.com/wiki/Relative_Vigor_Index_(RVI)/
    '''

    lines = ('rvi', 'signal')
    params = (('period', 10),)

    def __init__(self):
        self.addminperiod(self.params.period)
        self.high_low_diff = self.data.high - self.data.low
        self.open_close_diff = self.data.close - self.data.open
        self.sum_hl = bt.indicators.SumN(self.high_low_diff, period=self.params.period)
        self.sum_oc = bt.indicators.SumN(self.open_close_diff, period=self.params.period)
        self.rvi = 100 * self.sum_oc / self.sum_hl
        self.signal = bt.indicators.SMA(self.rvi, period=4)