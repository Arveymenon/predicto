import pandas as pd
import multiprocessing as mp
import ctypes

from shortlisting.multiprocessedShortlisting import multiProcessedShortlisting
# from algorithms.Strategies.MovingAverageCrossover.Strategy import Strategy
# from algorithms.Strategies.Shortlisting.Volitility import VolatilityStrategy

# from algorithms.Strategies.Shortlisting.InsideDay.InsideDay import InsideDayStrategy
# from algorithms.Strategies.Shortlisting.SmaRsi.SmaRsi import SMARSI_Strategy
# from datetime import datetime, timedelta

# shortlisted_stocks = list()


# from backtesting.backtest import backtest
from shortlisting.shortlisting import shortlist
from configuration import getConfig

class Shortlist:

    def __init__(self, config: dict) -> None:

        manager = mp.Manager()
        self.shortlisted_stocks = manager.list([])

        dataSetFileName = config["input_file"]
        shortlistStrategy = config["shortlisting"]["strategyName"]
        
        df = pd.read_csv(r'./data/'+dataSetFileName+'.csv')
        df['Symbol'] = 'NSE:'+ df['Symbol']
        symbols = df['Symbol'].to_list()

        datetime_format = config["shortlisting"]["interval"]["datetime_format"]
        interval = config["shortlisting"]["interval"]["intervals"]

        shortlistingTimeFrame = [
            config["shortlisting"]["interval"]["start_datetime"],
            config["shortlisting"]["interval"]["end_datetime"]
        ]

        multiProcessedShortlisting(
            symbols,
            shortlistingTimeFrame, datetime_format, interval,
            config["shortlisting"]["strategy"],
            self.shortlisted_stocks,
            plot=config["shortlisting"]["plot"]
        )

        # for symbol in symbols:
        #     shortlist(
        #         symbol,
        #         shortlistingTimeFrame[0], shortlistingTimeFrame[1], datetime_format, interval,
        #         config["shortlisting"]["strategy"],
        #         self.shortlisted_stocks,
        #         plot=config["shortlisting"]["plot"]
        #     )

        print(self.shortlisted_stocks)
        df = pd.DataFrame(list(self.shortlisted_stocks), columns = ["Symbol", "High"])


        df.to_csv("./data/responseData/shortlist/"+shortlistStrategy+"."+dataSetFileName+".csv")

        print(shortlistingTimeFrame)
        print("----------------------------------------------------------shortlisting end----------------------------------------------------------")