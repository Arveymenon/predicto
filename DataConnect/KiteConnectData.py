from audioop import reverse
import pandas
from kite_connect.main import KiteConnect
import backtrader as bt

from datetime import datetime
import pandas as pd

class KiteConnectData():

    def __init__(self, datetime_format, symbol, fromDate, toDate, intervals):
        self.success = False

        # Using custom kite connect
        kite = KiteConnect().kite

        # instruments = pandas.DataFrame(kite.instruments())
        # instruments.to_csv(r'./data/instruments.csv')

        instruments = pd.read_csv(r'./data/instruments.csv')
        
        exchange = symbol.split(":")[0]
        tradingsymbol = symbol.split(":")[1]
        self.datas = []

        try:
            instrument_token = instruments[
                                    (instruments.tradingsymbol == tradingsymbol) & 
                                    (instruments.exchange == exchange)].instrument_token.values[0]
        
            # # END-------------------------

            path = './data/temp/'+ tradingsymbol

            for interval in intervals:

                df1 = pandas.DataFrame(kite.historical_data(instrument_token, from_date=fromDate, to_date=toDate, interval=interval, oi=True))
                df1.to_csv(path+"-"+interval+".csv",index=False)

                data = bt.feeds.GenericCSVData(
                    dataname = path+"-"+interval+".csv",
                    fromdate=datetime.strptime(fromDate, datetime_format),
                    todate=datetime.strptime(toDate, datetime_format),
                    dtformat=(datetime_format),
                    time=-1,
                    datetime= 0,

                    reverse=False,
                    adjclose=False,
                    adjvolume=False,
                    timeframe=bt.TimeFrame.Minutes,
                )
                self.datas.append(data)

            self.success = True
        except:
            print('Some error occoured for %s', symbol)