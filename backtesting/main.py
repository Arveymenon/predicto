import pandas as pd
from backtesting import multiprocessedBacktesting
from algorithms.Strategies.MACD.Strategy import Strategy
from datetime import datetime, timedelta

from backtesting.backtest import backtest

class Backtesting:

    def __init__(self) -> None:

        df = pd.read_csv(r'./data/volitileStocks.csv')
        df['Symbol'] = 'NSE:'+ df['Symbol']
        symbols = df['Symbol'].to_list()
        symbol = 'NSE:NIFTY BANK'

        datetime_format = "%Y-%m-%d %H:%M:%S"
        interval = ["5minute"]

        backtestTimeFrame = [
            (datetime.now() - timedelta(days = 30)).strftime(datetime_format),
            (datetime.now() - timedelta(days = 0)).strftime(datetime_format)
        ]

        forwardTimeFrame = [
            (datetime.now() - timedelta(days = 30)).strftime(datetime_format),
            (datetime.now() - timedelta(days = 0)).strftime(datetime_format)
        ]

        # multiprocessedBacktesting.multiProcessedBacktest(symbols, datetime_format, interval, Strategy, backtestTimeFrame,True, forwardTimeFrame)
        backtest(symbol, backtestTimeFrame[0], backtestTimeFrame[1], datetime_format, interval, Strategy)