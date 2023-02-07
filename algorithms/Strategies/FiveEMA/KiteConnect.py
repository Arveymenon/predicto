from audioop import reverse
import pandas
from kite_connect.main import KiteConnect
import backtrader as bt

from datetime import datetime

interval = "1d"  #1 days interval

class KiteConnectData():

    def __init__(self, time_format, symbol, fromDate, toDate, interval):

        # Using custom kite connect
        kite = KiteConnect().kite

        instruments = pandas.DataFrame(kite.instruments())
        
        exchange = symbol.split(":")[0]
        tradingsymbol = symbol.split(":")[1]
        
        instrument_token = instruments[
                                    (instruments.tradingsymbol == tradingsymbol) & 
                                    (instruments.exchange == exchange)].instrument_token.values[0]
        # # END-------------------------

        path = './data/temp/'+ tradingsymbol

        df1 = pandas.DataFrame(kite.historical_data(instrument_token, from_date=fromDate, to_date=toDate, interval=interval[0], oi=True))
        df1['Datetime'] = pandas.to_datetime(df1['Datetime'], format=time_format)
        df1.to_csv(path+"-"+interval[0]+".csv",index=False)
        
        df2 = pandas.DataFrame(kite.historical_data(instrument_token, from_date=fromDate, to_date=toDate, interval=interval[1], oi=True))
        df2['Datetime'] = pandas.to_datetime(df2['Datetime'], format=time_format)
        df2.to_csv(path+"-"+interval[1]+".csv",index=False)
        
        self.data = bt.feeds.BacktraderCSVData(
            dataname = path+"-"+interval[0]+".csv",
            fromdate=datetime.strptime(fromDate, time_format),
            todate=datetime.strptime(toDate, time_format),
            dtformat=(time_format),
            tmformat=('%H:%M:%S'),
            time=-1,

            datetime= 0,

            reverse=False,
            adjclose=False,
            adjvolume=False,
            timeframe=bt.TimeFrame.Minutes,
            compression=5,
        )
        
        self.data2 = bt.feeds.BacktraderCSVData(
            dataname = path+"-"+interval[1]+".csv",
            fromdate=datetime.strptime(fromDate, time_format),
            todate=datetime.strptime(toDate, time_format),
            tmformat=('%H:%M:%S'),
            time=-1,

            datetime= 0,
            
            reverse=False,
            adjclose=False,
            adjvolume=False,
            timeframe=bt.TimeFrame.Minutes,
            compression=15
        )

        self.datas = [
            self.data2,
            self.data
        ]