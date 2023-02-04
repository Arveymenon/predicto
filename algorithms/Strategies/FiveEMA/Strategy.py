# This strategy use a Trailing Stop loss of 1%

from datetime import datetime
import backtrader as bt

# Create a Stratey
class Strategy(bt.Strategy):

    def log(self, txt, dt=None):
        ''' Logging function fot this strategy'''
        dt = dt or self.datas[0].datetime.date()
        print('%s, %s' % (dt.format("%Y-%m-%d %H:%M:%S"), txt))

    def __init__(self):
        self.data_5min_close = self.datas[0].close
        self.data_15min_close = self.datas[1].close
        self.ema_5min = bt.indicators.ExponentialMovingAverage(self.data_5min_close, period=5)
        self.ema_15min = bt.indicators.ExponentialMovingAverage(self.data_15min_close, period=5)
        print("Initial Broker Cash", self.broker.cash)
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

        self.order = None


    def next(self):
        
        if not self.position:
            if self.data_5min_close[0] > self.ema_5min[0] and self.data_15min_close[0] > self.ema_15min[0]:
                self.buy()
        elif self.data_5min_close[0] < self.ema_5min[0] and self.data_15min_close[0] < self.ema_15min[0]:
            self.sell()

    def stop(self):
        print(self.count)
