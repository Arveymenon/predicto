import backtrader as bt

class TotalValueAnalyzer(bt.Analyzer):
    def __init__(self):
        self.portfolio_value = []

    def start(self):
        self.portfolio_value = []

    def next(self):
        portfolio_value = self.strategy.cerebro.broker.getvalue()
        self.portfolio_value.append(portfolio_value)

    def stop(self):
        self.total_value = self.portfolio_value[-1]
        print(f"Final portfolio value: {self.portfolio_value[-1]:.2f}")