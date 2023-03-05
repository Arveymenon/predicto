import backtrader as bt

class VolatilityStrategy(bt.Strategy):
    
    params = dict(
        bollinger_period=20, # Bollinger Bands period
        bollinger_dev=2, # Bollinger Bands standard deviation
        atr_period=14, # ATR period
        rvi_period=10, # RVI period
        rvi_signal=4 # RVI signal period
    )

    def _init_(self):
        self.bollinger = bt.indicators.BollingerBands(self.data.close, period=self.params.bollinger_period, devfactor=self.params.bollinger_dev)
        self.atr = bt.indicators.ATR(self.data, period=self.params.atr_period)
        self.rvi = bt.indicators.RVI(self.data, period=self.params.rvi_period, signalperiod=self.params.rvi_signal)
        self.trade_on = False
        
    def next(self):
        if self.data.close > self.bollinger.lines.top and self.atr > self.atr[1] and self.rvi > self.rvi.signal:
            self.trade_on = True
            
    def stop(self):
        if self.trade_on:
            print(f"{self.data._name} is worth trading on")
        else:
            print(f"{self.data._name} is not worth trading on")