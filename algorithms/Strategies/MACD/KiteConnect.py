from audioop import reverse
import pandas
from kite_connect.main import KiteConnect
import backtrader as bt

from datetime import datetime

interval = "1d"  #1 days interval

class KiteConnectData():

    def __init__(self, datetime_format, symbol, fromDate, toDate, interval):
        self.success = False

        # Using custom kite connect
        kite = KiteConnect().kite

        instruments = pandas.DataFrame(kite.instruments())
        
        exchange = symbol.split(":")[0]
        tradingsymbol = symbol.split(":")[1]

        try:
            instrument_token = instruments[
                                    (instruments.tradingsymbol == tradingsymbol) & 
                                    (instruments.exchange == exchange)].instrument_token.values[0]
        
            # # END-------------------------

            path = './data/temp/'+ tradingsymbol

            df1 = pandas.DataFrame(kite.historical_data(instrument_token, from_date=fromDate, to_date=toDate, interval=interval[0], oi=True))
            # df1['Datetime'] = pandas.to_datetime(df1['Datetime'], format=datetime_format)
            df1.to_csv(path+"-"+interval[0]+".csv",index=False)

            self.data = bt.feeds.BacktraderCSVData(
                dataname = path+"-"+interval[0]+".csv",
                fromdate=datetime.strptime(fromDate, datetime_format),
                todate=datetime.strptime(toDate, datetime_format),
                dtformat=(datetime_format),
                time=-1,

                datetime= 0,

                reverse=False,
                adjclose=False,
                adjvolume=False,
                timeframe=bt.TimeFrame.Minutes,
                compression=5,
            )

            self.datas = [self.data]
            self.success = True
        except:
            print('Some error occoured for %s', symbol)