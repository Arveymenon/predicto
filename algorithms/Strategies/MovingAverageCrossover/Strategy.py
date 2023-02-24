# This strategy use a 
# @param @trailing_stop loss of 2%

import backtrader as bt

# Create a Stratey
class Strategy(bt.Strategy):
    params = (
        ("fast", 9),
        ("slow", 18),
        ("stop_loss", 0.10),
        ("take_profit", 0.20),
        ("trailing_stop", True)
    )

    def log(self, txt, dt=None):
        ''' Logging function fot this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        time = dt or self.datas[0].datetime.time()
        print('%s, %s, %s' % (dt.isoformat(), time, txt))

    def __init__(self):
        self.fast_ema = bt.indicators.EMA(self.data.close, period=self.params.fast)
        self.slow_ema = bt.indicators.EMA(self.data.close, period=self.params.slow)

        self.book_profit_price = 0.0
        self.stop_price= 0.0
        self.bought_at = 0.0

        self.profit = 0.0
        self.loss = 0.0

    def notify_order(self, order):
        if(order.status in [order.Submitted, order.Accepted]):
            return

        if(order.status in [order.Completed]):
            if (order.isbuy()):
                self.log("Buy Executed {}".format(order.executed.price))
                pass
            elif (order.issell()):
                if(order.executed.price > self.bought_at):
                    self.profit += order.executed.price - self.bought_at
                else:
                    self.loss += self.bought_at - order.executed.price

                self.log("Sell Executed {}".format(order.executed.price))

            self.bar_executed = len(self)

        self.order = None


    def next(self):
        if not self.position:
            if self.fast_ema[0] > self.slow_ema[0]:
                # size = int(self.broker.cash / self.data.close[0])
                self.buy()
        else:
            # trailing stop loss condition
            # if self.data.close[0] > self.stop_price:
            #     recom_stop_price = self.data.close[0] * (1 - self.params.stop_loss)
            #     self.stop_price = max(recom_stop_price, self.stop_price)
            # else:
            #     self.sell()

            # # book profit condition
            # if self.data.close[0] > self.book_profit_price:
            #     self.sell()
            
            # if ema indicator is hit
            if self.fast_ema[0] < self.slow_ema[0]:
                self.sell()

        if(str(self.datas[0].datetime.time()) == str('15:00:00')):
            print("Day end close")
            if(self.position.size < 0):
                self.close()
        

    def stop(self):
        print(self.position)
    # runs at the end