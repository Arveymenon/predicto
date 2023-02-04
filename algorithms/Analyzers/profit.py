import backtrader as bt

# Define a custom analyzer to keep track of profits
class ProfitAnalyzer(bt.Analyzer):
    def __init__(self):
        self.profit = 0.0
        self.order = None
        self.buyprice = None
        self.buycomm = None

    # def next(self):
    #     if (self.order.isbuy() or self.order.issell()) :
    #         self.profit += self.strategy.broker.getvalue() - self.strategy.broker.startingcash

    def next(self):
        if self.order:
            print("An order was completed")
            # Check if an order was placed
            if self.order.status == order.Completed:
                if self.order.isbuy():
                    self.buyprice = self.data.close[0]
                    self.buycomm = self.order.executed.comm
                else:
                    # Calculate the profit only if the buy or sell order was placed
                    self.profit = self.order.executed.value - self.buyprice * self.data.close[0]
                    self.order = None