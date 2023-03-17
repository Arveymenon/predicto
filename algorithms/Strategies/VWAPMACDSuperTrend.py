import backtrader as bt

from Indicators.VWAP import VWAP
from Indicators.SuperTrend import SuperTrend

from math import floor

class VWAPMACDSuperTrendStrategy(bt.Strategy):
    '''
    Sample strategy that uses the VWAP indicator
    '''
    def __init__(self):
        self.superTrend = SuperTrend(self.datas[0])
        self.vwap = VWAP(self.datas[0], period=6)
        self.macd = bt.indicators.MACD(period_me1=12, period_me2=26, period_signal=9)

        self.data.lines.vwap = self.vwap.lines.vwap
        self.order = None
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
        if self.order:
            return

        if self.data.low[0] > self.vwap[0]:
                size = floor(self.broker.cash/self.datas[0].close[0])
                self.order = self.buy(size=size, data=self.datas[0])
        elif self.data.low[0] < self.vwap[0]:
                size = floor(self.broker.cash/self.datas[0].close[0])
                self.order = self.sell(size=size, data=self.datas[0])
        
        # if self.data.close[0] > self.vwap[0] and self.data.close[-1] <= self.vwap[-1]:
        #     if self.position:
        #         self.close()
        #     else:
        #         self.order = self.buy()
        # elif self.data.close[0] < self.vwap[0] and self.data.close[-1] >= self.vwap[-1]:
        #     if self.position:
        #         self.close()
        #     else:
        #         self.order = self.sell()

    def notify_order(self, order):
        if order.status in [order.Completed, order.Cancelled, order.Rejected]:
            self.order = None
    