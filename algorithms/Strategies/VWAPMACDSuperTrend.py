import backtrader as bt

from Indicators.VWAP import VWAP
from Indicators.SuperTrend import SuperTrend

from math import floor

class VWAPMACDSuperTrendStrategy(bt.Strategy):
    '''
    Sample strategy that uses the VWAP indicator
    '''
    def __init__(self):
        self.vwap = VWAP(self.datas[0], period=6)
        self.macd = bt.indicators.MACD(period_me1=12, period_me2=26, period_signal=9)

        self.superTrend = SuperTrend(self.datas[0])
        self.dclose = self.datas[0].close
        self.cross = bt.ind.CrossOver(self.dclose, self.superTrend)
        

        self.data.lines.vwap = self.vwap.lines.vwap
        self.order = None
        self.trades = []

    # @Override
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

    # @Override
    def next(self):
        if self.order:
            return

        VWAPSignal = 1 if type(self.confirmVWAP()) else 0
        SuperTrendSignal = 1 if type(self.confirmSuperTrend()) == str else 0
        MACDSignal = 1 if type(self.confirmMACD()) == str else 0

        if VWAPSignal + SuperTrendSignal + MACDSignal >= 2:
            trade_type = self.confirmVWAP() or self.confirmSuperTrend()

            if trade_type == 'buy' :
                if self.position:
                    self.close()
                else:
                    size = floor(self.broker.cash/self.datas[0].close[0])
                    self.order = self.buy(size=size, data=self.datas[0])

            if trade_type == 'sell' :
                if self.position:
                    self.close()
                else:
                    size = floor(self.broker.cash/self.datas[0].close[0])
                    self.order = self.sell(size=size, data=self.datas[0])

        # important for day end closing
        if(str(self.datas[0].datetime.time()) == str('15:00:00')):
            self.trade = False

            print("Day end close")
            print("Day end value", self.broker.getvalue())
            if(self.position.size < 0):
                self.close()



    # @Override
    def notify_order(self, order):
        if order.status in [order.Completed, order.Cancelled, order.Rejected]:
            self.order = None
    
    def confirmVWAP(self):
        for i in range (0, 3):
            if self.data.close[0- i] > self.vwap[0- i] and self.data.close[-1 - i] <= self.vwap[-1 - i]:
                return 'buy'
            elif self.data.close[0- i] < self.vwap[0- i] and self.data.close[-1 - i] >= self.vwap[-1 - i]:
                return 'sell'
            pass

        return False

    def confirmSuperTrend(self):
        for i in range (0, 3):
            if self.cross[0 - i]==1 and self.position.size <= 0:
                return 'buy'
            elif self.cross[0 - i]==-1 and self.position.size >= 0:
                return 'sell'
            
        return False
    
    def confirmMACD(self):
        for i in range (0, 3):
            if self.cross[0 - i]==1 and self.position.size <= 0:
                return 'buy'
            elif self.cross[0 - i]==-1 and self.position.size >= 0:
                return 'sell'
            
        return False