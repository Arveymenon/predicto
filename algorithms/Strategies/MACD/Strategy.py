# This strategy uses ema set at 5 for 2 data sets
# also only executes trades based on 
#   if the previous ema crossed 

from datetime import datetime, timedelta
import backtrader as bt
import pandas as pd
from pytz import timezone

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

        self.macd = bt.indicators.MACD(
            period_me1=self.p.fast_length,
            period_me2=self.p.slow_length,
            period_signal=self.p.signal_length,
        )
        
    def notify_order(self, order):
        # if(order.status in [order.Submitted, order.Accepted]):
        #     return

        if(order.status in [order.Completed]):
            # self.log("Executed {}".format(order.executed.price))
            self.order = None
            if (order.isbuy()):

                recom_stop_price = self.data.close[0] * (1 - self.params.stop_loss)
                self.stop_price = max(recom_stop_price, self.stop_price)

            elif (order.issell()):
                self.stop_price = 0.0


        pass

    def next(self):
        ### comment this block and might need to remove self.order from store buy() and sell() in self.order to enable short selling
        # if self.order:
        #     return
        ### ----------------------------------------------
        # self.data.close[0] > self.atr[-1] * self.params.atr_multiplier:
        
        if self.macd.lines.macd[0] > self.macd.lines.signal[0] and \
            self.macd.lines.macd[-1] <= self.macd.lines.signal[-1]:
            # Buy signal
            self.buy(size = 1)

        else:
            # trailing stop loss condition
            # if self.data.close[0] > self.stop_price:
            #     recom_stop_price = self.data.close[0] * (1 - self.params.stop_loss)
            #     self.stop_price = max(recom_stop_price, self.stop_price)
            # else:
            #     self.sell()
                
            if self.macd.lines.macd[0] < self.macd.lines.signal[0] and \
                self.macd.lines.macd[-1] >= self.macd.lines.signal[-1]:
                # Sell signal
                self.close()
            

        # Day end closing
        # if(str(self.datas[0].datetime.time()) == str('15:00:00')):
        #     self.close()
        #     self.day = self.day + 1

    def stop(self):
        pass
