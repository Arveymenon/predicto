import pandas as pd
from backtesting import multiprocessedBacktesting
# from algorithms.Strategies.MovingAverageCrossover.Strategy import Strategy
from algorithms.Strategies.Shortlisting.InsideDay.InsideDay import InsideDayStrategy
from algorithms.Strategies.Shortlisting.SmaRsi.SmaRsi import SMARSI_Strategy
from datetime import datetime, timedelta


# from backtesting.backtest import backtest
from shortlisting.shortlisting import shortlist, shortlisted_stocks
from configuration import config

dataSetFileName = config["input_file"]
shortlistStrategy = config["shortlisting"]["strategyName"]

class Shortlist:

    def __init__(self) -> None:

        df = pd.read_csv(r'./data/'+dataSetFileName+'.csv')
        df['Symbol'] = 'NSE:'+ df['Symbol']
        symbols = df['Symbol'].to_list()
        # symbols = ["NSE:AUROPHARMA"]

        # symbol = 'NSE:ADANIENT'
        # symbol = 'NSE:GAIL'

        datetime_format = "%Y-%m-%d %H:%M:%S"
        interval = ["day"]

        backtestTimeFrame = [
            (datetime.now() - timedelta(days = 180)).strftime(datetime_format),
            (datetime.now() - timedelta(days = 173)).strftime(datetime_format)
        ]

        for symbol in symbols:
            shortlist(
                symbol,
                backtestTimeFrame[0], backtestTimeFrame[1], datetime_format, interval,
                InsideDayStrategy,
                plot=False
            )

        print(shortlisted_stocks)
        df = pd.DataFrame([], columns = ["Symbol"])

        if len(shortlisted_stocks) > 0:
            print(pd.Series(shortlisted_stocks).str.split(":").str[1])
            df["Symbol"] = pd.Series(shortlisted_stocks).str.split(":").str[1]

        df.to_csv("./data/responseData/shortlist/"+shortlistStrategy+"."+dataSetFileName+".csv")
