# Should be used for intraday trading.
# Hence has a shorter time interval of weeks in the data used.

from datetime import datetime, timedelta

import numpy as np
from pandas import DataFrame
import yfinance as yf

from algorithms.Analyzers.profit import ProfitAnalyzer

import backtrader as bt
from algorithms.Strategies.FiveEMA.Strategy import Strategy

from generateData import GenerateData


INITIAL_INVESTMENT = 100000
COMMISSION = 0.002

class RunTechnicalAnalysis5EMA():   
    
    def backtest(self, symbol, initialInvestment=INITIAL_INVESTMENT):
        # Backtesting 
        print("Backtesting: started")
        cerebro = bt.Cerebro()
        cerebro.broker.setcash(initialInvestment)
        cerebro.broker.setcommission(commission=COMMISSION)
        print("Backtesting: using 5 days old data")
        
        generateData = GenerateData()

        period = "1mo"
        #-------------------- data set --------------------------

        dataname1 = generateData.createData(symbol, interval="15m", period=period)
        dataname2 = generateData.createData(symbol, interval ="5m", period=period)

        data1 = bt.feeds.YahooFinanceCSVData(
            dataname = dataname1,
            reverse=False
        )

        data2 = bt.feeds.YahooFinanceCSVData(
            dataname = dataname2,
            reverse=False
        )

        cerebro.adddata(data1)
        cerebro.adddata(data2)
        #-------------------- data set end --------------------------

        # Define the optimization parameters and ranges
        cerebro.addstrategy(Strategy)
        # cerebro.optstrategy(Strategy)
        cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name="TAnalyzer")


        print('Backtesting: Starting portfolio Value: %.2f' % cerebro.broker.getvalue())

        results = cerebro.run()
        # cerebro.plot()
        # print(results[0][0].analyzers.TAnalyzer.get_analysis())

        # suggested_df = self.getIdealParams(results)
        # self.fast_ema = suggested_df['fast'].head(10).values
        # self.slow_ema = suggested_df['slow'].head(10).values

        print('Backtesting: Final portfolio Value: %.2f' % cerebro.broker.getvalue())
        print("Backtesting: ended")
    

    def __init__(self, data: DataFrame) -> None:
        # NSE index
        # self.backtest(symbol="^NSEI")

        #
        self.backtest(symbol="ADANIGREEN.NS")
        # self.backtest(symbol="WIPRO.NS")
        pass
