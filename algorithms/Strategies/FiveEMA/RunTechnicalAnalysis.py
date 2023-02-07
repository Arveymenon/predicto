# Should be used for intraday trading.
# Hence has a shorter time interval of weeks in the data used.

from datetime import datetime, timedelta

import numpy as np
from pandas import DataFrame
import yfinance as yf

from algorithms.Analyzers.profit import ProfitAnalyzer

import backtrader as bt
from algorithms.Strategies.FiveEMA.KiteConnect import KiteConnectData
from algorithms.Strategies.FiveEMA.Strategy import Strategy

from algorithms.Strategies.FiveEMA.ResampleData import ResampledData
from generateData import GenerateData


INITIAL_INVESTMENT = 100000
COMMISSION = 0.002

class RunTechnicalAnalysis: 
    
    def backtest(self, symbol, initialInvestment=INITIAL_INVESTMENT):
        # Backtesting 
        print("Backtesting: started")
        cerebro = bt.Cerebro()
        cerebro.broker.setcash(initialInvestment)
        cerebro.broker.setcommission(commission=COMMISSION)
        
        time_format = "%Y-%m-%d %H:%M:%S"
        days = 30
        print(f"Backtesting: using {days} days old data")
    #---------------------Kite Data -------------------------#

        start_date = (datetime.now() - timedelta(days = days)).strftime(time_format)
        end_date = (datetime.now()).strftime(time_format)

        kiteConnectData = KiteConnectData(time_format, symbol, fromDate=start_date, toDate=end_date, interval = ["5minute", "15minute"])

        cerebro.adddata(kiteConnectData.data)
        cerebro.adddata(kiteConnectData.data2)

    #-------------------- Yahoo financee data --------------------------#
        # generateData = GenerateData()
        # period = "1mo"
        # dataname1 = generateData.createData(symbol, interval="5m", period=period)
        # dataname2 = generateData.createData(symbol, interval ="15m", period=period)

        # data1 = bt.feeds.BacktraderCSVData(
        #     dataname = dataname1,
        #     reverse=False
        # )

        # data2 = bt.feeds.BacktraderCSVData(
        #     dataname = dataname2,
        #     reverse=False
        # )

        # cerebro.adddata(data1)
        # cerebro.adddata(data2)
    #-------------------- data set end --------------------------#

        # # Define the optimization parameters and ranges
        cerebro.addstrategy(Strategy)
        # cerebro.optstrategy(Strategy)
        # cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name="TAnalyzer")


        print('Backtesting: Starting portfolio Value: %.2f' % cerebro.broker.getvalue())

        cerebro.run()
        # cerebro.plot(iplot=True, volume=False, style='bar', rows=2, cols=1, name=['5min', '15min'])

        print('Backtesting: Final portfolio Value: %.2f' % cerebro.broker.getvalue())
    

    def __init__(self) -> None:
        # self.backtest(symbol="NFO:NIFTY23FEB16500CE")
        self.backtest(symbol="NSE:ADANIGREEN")
        # self.backtest(symbol="NSE:POLYCAB")
        # self.backtest(symbol="NSE:NIFTYBEES")

        #---- for yahoo finance data
        # NSE index
        # self.backtest(symbol="^NSEI")
        # self.backtest(symbol="HDFC.NS")
        #
        # self.backtest(symbol="ADANIGREEN.NS")
        # self.backtest(symbol="WIPRO.NS")
