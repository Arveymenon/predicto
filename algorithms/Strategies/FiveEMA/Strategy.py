# This strategy uses ema set at 5 for 2 data sets
# also only executes trades based on 
#   if the previous ema crossed 

from datetime import datetime
import backtrader as bt

# Create a Stratey
class Strategy(bt.Strategy):

    def log(self, txt, dt=None):
        ''' Logging function fot this strategy'''
        dt = dt or self.datas[0].datetime.date()
        print('%s, %s' % (dt.format("%Y-%m-%d %H:%M:%S"), txt))

    def __init__(self):
        self.data_5min_low = self.datas[0].low
        self.data_15min_high = self.datas[1].high
        self.ema_5min = bt.indicators.ExponentialMovingAverage(self.data_5min_low, period=5)
        self.ema_15min = bt.indicators.ExponentialMovingAverage(self.data_15min_high, period=5)
        self.count = 0

    def notify_order(self, order):
        if(order.status in [order.Submitted, order.Accepted]):
            return
        if(order.status in [order.Completed]):
            if (order.isbuy()):
                # self.log("Buy Executed {}".format(order.executed.price))
                self.count += 1
            elif (order.issell()):
                self.count -= 1

            self.bar_executed = len(self)
        


    def next(self):
        if not self.position:
            if (self.data_15min_high[-1] < self.ema_15min[-1] and self.data_15min_high[0] > self.ema_15min[0]):
                self.buy()
        else:
            if self.data_5min_low[0] < self.ema_5min[0] and self.data_5min_low[-1] > self.ema_5min[-1]:
                self.sell()

    def stop(self):
        print(self.count)
