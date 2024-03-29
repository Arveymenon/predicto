import backtrader as bt
import pandas as pd

from Indicators.SuperTrend import SuperTrend

from math import floor

class SupertrendStrategy(bt.Strategy):
    params = (
        ('stop_loss', 0.002),
        ('book_profit', 0.06)
    )

    def log(self, txt, dt=None):
        if  True:
            dt = dt or self.datas[0].datetime.date(0)
            print('%s - %s' % (dt.isoformat(), txt))
 
    def __init__(self):
        self.x = SuperTrend(self.data)
        self.dclose = self.datas[0].close
        self.cross = bt.ind.CrossOver(self.dclose, self.x) 
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
            
    def notify(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return
        # Check if an order has been completed
        # Attention: broker could reject order if not enougth cash
        if order.status in [order.Completed, order.Canceled, order.Margin]:
            if order.isbuy():
                self.log(
                    'BUY EXECUTED: %s, Price: %.2f, Cost: %.2f, Comm %.2f' %
                    (order.data._name,
                     order.executed.price,
                     order.executed.value,
                     order.executed.comm))
                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
                self.opsize = order.executed.size

                self.trades.append([self.datas[0].datetime.datetime(), "buy", order.executed.size, order.executed.price])
            else:  # Sell
                self.log('SELL EXECUTED: %s, Price: %.2f, Cost: %.2f, Comm %.2f' %
                         (order.data._name,
                          order.executed.price,
                          order.executed.value,
                          order.executed.comm))
                
                self.trades.append([self.datas[0].datetime.datetime(), "sell", order.executed.size, order.executed.price])
                
    def next(self):

        if self.cross[0]==1:
            # self.order_target_percent(data=self.data, target=1)
            if(not self.position):
                size = floor(self.broker.cash/self.datas[0].close[0])
                self.order = self.buy(size=size, data=self.datas[0])
            elif(self.position.size < 0):
                self.close()
        elif self.cross[0]==-1:
            if(not self.position):
                size = floor(self.broker.cash/self.datas[0].close[0])
                self.order = self.sell(size=size, data=self.datas[0])
            elif(self.position.size > 0):
                self.close()

        
        # Stop Loss And Book Profit
        if(self.position):
            last_trade_price = self.trades[-1][3]

            if self.position.size > 0:
                stop_loss = last_trade_price - self.params.stop_loss*last_trade_price
                if(self.datas[0].close[0] <= stop_loss):
                    self.close()

                book_profit = last_trade_price - self.params.book_profit*last_trade_price
                if(self.datas[0].close[0] >= book_profit):
                    print(self.datas[0].close[0])
                    self.trade = False
                    self.close()

            if self.position.size < 0:
                stop_loss = last_trade_price + self.params.stop_loss*last_trade_price
                if(self.datas[0].close[0] > stop_loss):
                    self.close()

                book_profit = last_trade_price - self.params.book_profit*last_trade_price
                if(self.datas[0].close[0] <= book_profit):
                    print(self.datas[0].close[0])
                    self.trade = False
                    self.close()

    
    def stop(self):
        all_trades = pd.DataFrame(self.trades,columns=["datetime",'type', "size", "price"])
        print("trades",all_trades)
        print("Position", self.position)