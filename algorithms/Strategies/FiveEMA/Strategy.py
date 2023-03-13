# This strategy uses ema set at 5 for 2 data sets
# also only executes trades based on 
#   if the previous ema crossed 

from datetime import datetime, timedelta
import backtrader as bt
import pandas as pd
from pytz import timezone
from math import floor

# Create a Stratey
class Strategy(bt.Strategy):

    def log(self, txt, dt=None):
        ''' Logging function fot this strategy'''
        dt = dt or self.datas[0].datetime.date()
        # ('%s, %s' % (dt.format("%Y-%m-%d %H:%M:%S"), txt))

    def __init__(self):
        self.data_5min_low = self.datas[0].low
        self.data_15min_high = self.datas[1].high

        self.ema_5min = bt.indicators.ExponentialMovingAverage(self.data_5min_low, period=5, plotname='5 min ema')
        self.ema_15min = bt.indicators.ExponentialMovingAverage(self.data_15min_high, period=5, plotname='15 min ema')
        self.count = 0
        self.order = None

    def notify_order(self, order):
        if(order.status in [order.Submitted, order.Accepted]):
            return
        if(order.status in [order.Completed]):
            # self.log("Executed {}".format(order.executed.price))
            self.order = None
            if (order.isbuy()):
                print("Bought ", self.position.size, "at ", order.executed.price, "on")
                self.count += 1
            elif (order.issell()):
                self.count -= 1
                print("Sold ", order.executed.size, "at ", order.executed.price, "on")

            print(self.datas[0].datetime.datetime())
            
            # commission_info = self.broker.getcommissioninfo(data=order.data)
            # commission = commission_info.getcommission(size=order.executed.size,
            #                                             price=order.executed.price,
            #                                             pseudoexec=order.executed.pseudo)
            # print(f"Commission: {commission}")
            pass

        if order.status in [bt.Order.Margin, bt.Order.Expired, bt.Order.Rejected, bt.Order.Cancelled]:
                print("Order not executed------------------",order.status, self.order)
                self.order = None

    def next(self):

        ### comment this block to enable short selling
        # if self.order:
        #     return
        ### ----------------------------------------------

        if (not self.position):
            if (self.data_15min_high[-1] < self.ema_15min[-1] and self.data_15min_high[0] >= self.ema_15min[0]):
                size = floor(self.broker.cash/self.datas[1].close)
                self.order = self.buy(size=size)
        elif self.data_5min_low[0] < self.ema_5min[0] and self.data_5min_low[-1] > self.ema_5min[-1]:
                self.order = self.sell(size=self.position.size)

        if(str(self.datas[0].datetime.time()) == str('15:00:00')):
            print("Day end close")
            if(self.position.size < 0):
                self.close()

    def stop(self):
        print("Count:", self.count)
        print("Position", self.position)
