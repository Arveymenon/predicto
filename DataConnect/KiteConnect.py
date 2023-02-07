from kite_connect.main import KiteConnect
import backtrader as bt

class KiteConnectData(bt.feeds.LiveDataBase):
    params = (
        ('symbol', 'NSE:INFY'),
        ('interval', '1min'),
    )

    def __init__(self):

        # Using custom kite connect
        kite = KiteConnect().kite
        # END-------------------------

        self.data = kite.historical_data(self.params.symbol, interval=self.params.interval, from_date='2022-01-01', to_date='2022-12-31')
        self.datas = [bt.feeds.PandasData(dataname=self.data, fromdate=self.data.index[0], todate=self.data.index[-1])]