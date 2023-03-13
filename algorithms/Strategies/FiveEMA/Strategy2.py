# This strategy uses ema set at 5 for 2 data sets
# also only executes trades based on 
#   if the previous ema crossed 

from datetime import datetime, timedelta
import backtrader as bt
import pandas as pd
from pytz import timezone
from math import floor

# Create a Stratey
class Strategy2(bt.Strategy):
    params = (
        ('stop_loss', 0.01),
        ('book_profit', 0.03)
    )

    def log(self, txt, dt=None):
        ''' Logging function fot this strategy'''
        dt = dt or self.datas[0].datetime.date()
        print('%s, %s' % (dt.format("%Y-%m-%d %H:%M:%S"), txt))

    def __init__(self):
        self.data_5min_low = self.datas[0].low
        self.data_15min_high = self.datas[1].high

        self.ema_5min = bt.indicators.ExponentialMovingAverage(self.data_5min_low, period=5, plotname='5 min ema')
        self.ema_15min = bt.indicators.ExponentialMovingAverage(self.data_15min_high, period=5, plotname='15 min ema')
        self.order = None
        self.trade = False
        self.trades = []

    def notify_order(self, order):
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

        if(str(self.datas[0].datetime.time()) == str('11:00:00')):
            self.trade = True

        # if(self.trade_today and self.day_count > 2):
        if(self.trade):
            if (self.data_15min_high[-1] < self.ema_15min[-1] and self.data_15min_high[0] >= self.ema_15min[0]):
                if(not self.position):
                    size = floor(self.broker.cash/self.datas[0].close[0])
                    self.order = self.buy(size=size, data=self.datas[0])
                elif(self.position.size < 0):
                    self.close()
            
            if self.data_5min_low[0] < self.ema_5min[0] and self.data_5min_low[-1] > self.ema_5min[-1]:
                    if(not self.position):
                        size = floor(self.broker.cash/self.datas[0].close[0])
                        self.order = self.sell(size=size, data=self.datas[0])
                    elif(self.position.size > 0):
                        self.close()

            # if(self.position):
                
                   
        
        # if(self.position):
        #     last_trade_price = self.trades[-1][3]

        #     if self.position.size > 0:
        #         stop_loss = last_trade_price - self.params.stop_loss*last_trade_price
        #         if(self.data_5min_low[0] <= stop_loss):
        #             self.close()

        #         book_profit = last_trade_price - self.params.book_profit*last_trade_price
        #         if(self.data_5min_low[0] >= book_profit):
        #             self.close()

        #     if self.position.size < 0:
        #         stop_loss = last_trade_price + self.params.stop_loss*last_trade_price
        #         if(self.data_5min_low[0] > stop_loss):
        #             self.close()

        #         book_profit = last_trade_price - self.params.book_profit*last_trade_price
        #         if(self.data_5min_low[0] > book_profit):
        #             self.close()


        # important for day end closing
        if(str(self.datas[0].datetime.time()) == str('15:00:00')):
            self.trade = False

            print("Day end close")
            print("Day end cash", self.broker.cash)
            print("Day end value", self.broker.getvalue())
            if(self.position.size < 0):
                self.close()

    def stop(self):
        all_trades = pd.DataFrame(self.trades,columns=["datetime",'type', "size", "price"])
        print("trades",all_trades)
        print("Position", self.position)
