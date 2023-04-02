from audioop import reverse
import pandas
from kite_connect.main import KiteConnect
import backtrader as bt

from datetime import datetime
import pandas as pd

interval = "1d"  #1 days interval

class KiteConnectData():

    def __init__(self, datetime_format, symbol, fromDate, toDate, interval):
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

            for inter in interval:

                df1 = pandas.DataFrame(kite.historical_data(instrument_token, from_date=fromDate, to_date=toDate, interval=inter, oi=True))
                df1.to_csv(path+"-"+inter+".csv",index=False)

                data = bt.feeds.GenericCSVData(
                    dataname = path+"-"+inter+".csv",
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


            # if(interval[1]):
            #     df2 = pandas.DataFrame(kite.historical_data(instrument_token, from_date=fromDate, to_date=toDate, interval=interval[1], oi=True))
            #     df2.to_csv(path+"-"+interval[1]+".csv",index=False)

            # self.data = bt.feeds.GenericCSVData(
            #     dataname = path+"-"+interval[0]+".csv",
            #     fromdate=datetime.strptime(fromDate, datetime_format),
            #     todate=datetime.strptime(toDate, datetime_format),
            #     dtformat=(datetime_format),
            #     time=-1,
            #     datetime= 0,

            #     reverse=False,
            #     adjclose=False,
            #     adjvolume=False,
            #     timeframe=bt.TimeFrame.Minutes,
            # )
            # if(interval[1]):
            #     self.data2 = bt.feeds.GenericCSVData(
            #         dataname = path+"-"+interval[1]+".csv",
            #         fromdate=datetime.strptime(fromDate, datetime_format),
            #         todate=datetime.strptime(toDate, datetime_format),
            #         dtformat=(datetime_format),
            #         time=-1,
            #         datetime= 0,

            #         reverse=False,
            #         adjclose=False,
            #         adjvolume=False,
            #         timeframe=bt.TimeFrame.Minutes
            #     )

            # self.datas = [self.data, self.data2]
            self.success = True
        except:
            print('Some error occoured for %s', symbol)