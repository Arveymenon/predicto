# This strategy uses ema set at 5 for 2 data sets
# also only executes trades based on 
#   if the previous ema crossed 

from datetime import datetime, timedelta
import backtrader as bt
import pandas as pd
from pytz import timezone

# Create a Stratey
class Strategy(bt.Strategy):

    def log(self, txt, dt=None):
        ''' Logging function fot this strategy'''
        dt = dt or self.datas[0].datetime.date()
        print('%s, %s' % (dt.format("%Y-%m-%d %H:%M:%S%z"), txt))

    def __init__(self):
        self.order = None
        self.data_close = self.datas[0].close
        self.macd = bt.indicators.MACD(self.data, plotname='5 min ema')
        
    def notify_order(self, order):
        if(order.status in [order.Submitted, order.Accepted]):
            return
        if(order.status in [order.Completed]):
            # self.log("Executed {}".format(order.executed.price))
            self.order = None
            if (order.isbuy()):
                print("Bought ", self.position.size, "at ", order.executed.price, "on")
            elif (order.issell()):
                print("Sold ", self.position.size, "at ", order.executed.price, "on")

            print(self.datas[0].datetime.datetime())
            # self.bar_executed = len(self)
            pass

        if order.status in [bt.Order.Margin, bt.Order.Expired, bt.Order.Rejected, bt.Order.Cancelled]:
                print("Order not executed------------------",order.status, self.order)
                self.order = None

    def next(self):

        ### comment this block and might need to remove self.order from store buy() and sell() in self.order to enable short selling
        if self.order:
            return
        ### ----------------------------------------------
        if not self.position:
            if (self.macd.macd[0] > self.macd.signal[0]) and (self.macd.macd[-1] < self.macd.signal[-1]):
                self.order = self.buy()
        else:
            if (self.macd.macd[0] < self.macd.signal[0]) and (self.macd.macd[-1] > self.macd.signal[-1]):
                self.order = self.close()

    def stop(self):
        # print("Count:", self.count)
        print("Position", self.position)
