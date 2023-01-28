import pandas as pd
import backtrader as bt

# Import the data into a pandas DataFrame
df = pd.read_csv("data/NSE100StockData/ACC.NShistorical_data.csv", delimiter=",", index_col="date", parse_dates= True)

# Create a Backtrader data feed
data = bt.feeds.PandasData(dataname=df)

class MyStrategy(bt.Strategy):
    params = (("fast", 7), ("slow", 20))

    def __init__(self):
        self.fast_ema = bt.indicators.EMA(period=self.params.fast)
        self.slow_ema = bt.indicators.EMA(period=self.params.slow)

    def next(self):
        if not self.position:
            if self.fast_ema > self.slow_ema:
                self.buy()
                self.stop_loss = self.data.close * 0.99
        else:
            if self.fast_ema < self.slow_ema:
                self.sell()
                self.stop_loss = None
            else:
                self.stop_loss = self.data.close * 0.99


# Create a Cerebro instance
cerebro = bt.Cerebro()

# Add the strategy to Cerebro
cerebro.addstrategy(MyStrategy)

# Add the Returns analyzer to Cerebro
cerebro.addanalyzer(bt.analyzers.Returns)

# Run the strategy
cerebro.run()


for analyzer in cerebro.analyzers:
    print(analyzer)

# Get the results of the Returns analyzer
for name, returns in filter(lambda x: x[1] == 'Returns', cerebro.analyzers):
    result = returns.get_analysis()
    # Print the profits
    print("Profits:", result['rtot'])