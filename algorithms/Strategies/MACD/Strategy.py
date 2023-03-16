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
    params = (
        ('fast_length', 12),
        ('slow_length', 26),
        ('signal_length', 9),
        ("stop_loss", 0.02)
    )

    def log(self, txt, dt=None):
        ''' Logging function fot this strategy'''
        dt = dt or self.datas[0].datetime.date()
        time = dt or self.datas[0].datetime.time()

    def __init__(self):
        self.day = 0

        # for short selling
        self.order = None

        # for trailing stoploss
        self.stop_price = 0.0
        self.trade = False
        self.trades = []

        self.macd = bt.indicators.MACD(
            period_me1=self.p.fast_length,
            period_me2=self.p.slow_length,
            period_signal=self.p.signal_length,
        )
        
    def notify_order(self, order):
        # if(order.status in [order.Submitted, order.Accepted]):
        #     return
        if(order.status in [order.Submitted, order.Accepted]):
            return
        
        if(order.status in [order.Completed]):
            # self.log("Executed {}".format(order.executed.price))
            self.order = None
            if (order.isbuy()):
                self.trades.append([self.datas[0].datetime.datetime(), "buy", order.executed.size, order.executed.price])
                print("Bought ", order.executed.size, "at ", order.executed.price, "on")
            elif (order.issell()):
                self.trades.append([self.datas[0].datetime.datetime(), "sell", order.executed.size, order.executed.price])
                print("Sold ", order.executed.size, "at ", order.executed.price, "on")

            print(self.datas[0].datetime.datetime())

        if order.status in [bt.Order.Margin, bt.Order.Expired, bt.Order.Rejected, bt.Order.Cancelled]:
                print("Order not executed------------------",order.status, self.order)
                self.order = None

    def next(self):
        ### comment this block and might need to remove self.order from store buy() and sell() in self.order to enable short selling
        # if self.order:
        #     return
        ### ----------------------------------------------
        # self.data.close[0] > self.atr[-1] * self.params.atr_multiplier:

        if(str(self.datas[0].datetime.time()) == str('11:00:00')):
            self.trade = True

        if(self.trade):
            if self.macd.lines.macd[0] > self.macd.lines.signal[0] and \
                self.macd.lines.macd[-1] <= self.macd.lines.signal[-1]:
                # Buy signal
                if(not self.position):
                    size = floor(self.broker.cash/self.datas[0].close[0])
                    self.order = self.buy(size=size, data=self.datas[0])
                elif(self.position.size < 0):
                    self.close()

            if self.macd.lines.macd[0] < self.macd.lines.signal[0] and \
                self.macd.lines.macd[-1] >= self.macd.lines.signal[-1]:
                # Sell signal
                if(not self.position):
                    size = floor(self.broker.cash/self.datas[0].close[0])
                    self.order = self.sell(size=size, data=self.datas[0])
                elif(self.position.size > 0):
                    self.close()
            

        # Day end closing
        if(str(self.datas[0].datetime.time()) == str('15:00:00')):
            self.trade = False

            print("Day end close")
            print("Day end value", self.broker.getvalue())
            if(self.position.size < 0):
                self.close()

    def stop(self):
        pass
