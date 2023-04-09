
import backtrader as bt
from datetime import datetime, timedelta
import pandas as pd
from kite_connect.main import KiteConnect

from kite_connect.kiteTicker import KiteTicker

kite = KiteConnect().kite

class LiveDataFeed(bt.feeds.DataBase):

    def __init__(self, symbol, fromDate, toDate, intervals):
        # initialize data feed with appropriate parameters
        self.fromdate = fromDate
        self.toDate = toDate
        self.intervals = intervals

        instruments = pd.read_csv(r'./data/instruments.csv')
        exchange = symbol.split(":")[0]
        tradingsymbol = symbol.split(":")[1]
        self.datas = []

        self.instrument_token = instruments[
                                    (instruments.tradingsymbol == tradingsymbol) & 
                                    (instruments.exchange == exchange)].instrument_token.values[0]

        for interval in intervals:
            data = pd.DataFrame(kite.historical_data(self.instrument_token, from_date=fromDate, to_date=toDate, interval=interval, oi=True))
            self.datas.append(bt.feeds.PandasData(data)) # Placeholder for actual data
            # self.data = bt.feeds.PandasData(dataname=df1)  

        
    def start(self):
        # start the data feed
        self.update_data()
        
    def update_data(self):
        # make API call to retrieve new data
        # assuming you have a function called fetch_new_data that retrieves the new data
        new_data = self.fetch_new_data()
        
        # update the data feed with the new data
        self.data = bt.feeds.PandasData(dataname=new_data)

    def fetch_new_data(self):

        # TODO: add 5 mins to toDate
        for interval in self.intervals:
            data = pd.DataFrame(kite.historical_data(self.instrument_token, from_date=self.fromDate, to_date=self.toDate, interval=interval, oi=True))
            self.datas.append(bt.feeds.PandasData(data))
    


print("____________________________")
def on_ticks(self, ws, ticks):
        # Callback to receive ticks.
        print("Ticks: {}".format(ticks))

def on_connect(self, ws, response):
    # Callback on successful connect.
    # Subscribe to a list of instrument_tokens (RELIANCE and ACC here).
    ws.subscribe([738561, 5633])

    # Set RELIANCE to tick in `full` mode.
    ws.set_mode(ws.MODE_FULL, [738561])

def on_close(self, ws, code, reason):
    # On connection close stop the main loop
    # Reconnection will not happen after executing `ws.stop()`
    ws.stop()

def __init__(self, **kwargs):
    self.params.update(kwargs)
    self.lines.datetime = 0  # datetime is expected in Unix timestamp format
    self.data = None
    self.datetime = datetime.utcnow()  # set initial datetime value

    kws = KiteTicker()

    kws.on_ticks = self.on_ticks
    kws.on_connect = self.on_connect
    kws.on_close = self.on_close

    kws.connect()