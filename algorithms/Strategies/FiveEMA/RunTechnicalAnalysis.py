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

class RunTechnicalAnalysis5EMA():   
    
    def backtest(self, symbol = "LT.NS", initialInvestment=INITIAL_INVESTMENT):
        # Backtesting 
        print("Backtesting: started")
        cerebro = bt.Cerebro()
        cerebro.broker.setcash(initialInvestment)
        print("Backtesting: using 5 days old data")
        
        generateData = GenerateData()

        period = "5d"
        #-------------------- data set --------------------------

        dataname1 = generateData.createData(symbol, interval="15m", period=period)
        dataname2 = generateData.createData(symbol, interval ="5m", period = period)

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
        # cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name="TAnalyzer")


        print('Backtesting: Starting portfolio Value: %.2f' % cerebro.broker.getvalue())

        results = cerebro.run()

        # print(results[0][0].analyzers.TAnalyzer.get_analysis())

        # suggested_df = self.getIdealParams(results)
        # self.fast_ema = suggested_df['fast'].head(10).values
        # self.slow_ema = suggested_df['slow'].head(10).values

        print('Backtesting: Final portfolio Value: %.2f' % cerebro.broker.getvalue())
        print("Backtesting: ended")

    def forwardtest(self, symbol = "LT.NS", initialInvestment=INITIAL_INVESTMENT):
        print("Forwardtesting: started")
        cerebro = bt.Cerebro()
        cerebro.broker.setcash(initialInvestment)
        print("Forwardtesting: using 1 years old data")
        start_date = (datetime.now() - timedelta(days=365 * 1)).strftime("%Y-%m-%d")
        end_date = (datetime.now() - timedelta(days=365 * 0)).strftime("%Y-%m-%d")

        dataname = self.createData(symbol, startDate=start_date, endDate=end_date)

        data = bt.feeds.YahooFinanceCSVData(
            dataname = dataname,
            reverse=False
        )

        cerebro.adddata(data)
        
        cerebro.optstrategy(Strategy, fast = self.fast_ema, slow =  self.slow_ema)

        cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name="TAnalyzer")

        print('Forwardtesting: Starting portfolio Value: %.2f' % cerebro.broker.getvalue())

        results = cerebro.run()
        
        suggested_df = self.getIdealParams(results)

        print(suggested_df.iloc[0])

        print('Forwardtesting: Final portfolio Value:'+ str(cerebro.broker.getvalue()))
        print("Forwardtesting: end")

    def __init__(self, data: DataFrame) -> None:
        self.backtest(symbol="^NSEI")
        # self.forwardtest(symbol="^NSEI")
        pass
