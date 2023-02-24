# Should be used for intraday trading.
# Hence has a shorter time interval of weeks in the data used.

from datetime import datetime, timedelta

import backtrader as bt
from algorithms.Strategies.MACD.KiteConnect import KiteConnectData
from algorithms.Strategies.MACD.Strategy import Strategy
import pandas as pd

import multiprocessing

INITIAL_INVESTMENT = 100000
COMMISSION = 0.002


class RunTechnicalAnalysis: 

    def backtest(self, symbol, start_date, end_date, time_format, interval, initialInvestment=INITIAL_INVESTMENT):
        # Backtesting 
        print("Backtesting: started")
        cerebro = bt.Cerebro()
        cerebro.broker.setcash(initialInvestment)
        cerebro.broker.setcommission(commission=COMMISSION)
        
    #---------------------Kite Data -------------------------#
        self.kiteConnectData = KiteConnectData(time_format, symbol, fromDate=start_date, toDate=end_date, interval = interval)

        if self.kiteConnectData.success:

            cerebro.adddata(self.kiteConnectData.data)
            #-------------------- Kite data end --------------------------#

            # # Define the optimization parameters and ranges
            cerebro.addstrategy(Strategy)
            # cerebro.optstrategy(Strategy)
            # cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name="TAnalyzer")


            print('Backtesting: Starting portfolio Value: %.2f' % cerebro.broker.getvalue())

            cerebro.run()
            # cerebro.plot(iplot=True, volume=False, style='bar', rows=2, cols=1, name=['macd'])
            cerebro.plot(iplot=True, volume=False, style='bar')
            # cerebro.plot()

            print('Backtesting: Final portfolio Value: %.2f' % cerebro.broker.getvalue())

            return {"symbol": symbol, "value": cerebro.broker.getvalue()}
    

    def multiprocessedBacktest(self, symbols, time_format, interval):
         # ---------------------- Back testing ---------------------------#
        start_date = (datetime.now() - timedelta(days = 60)).strftime(time_format)
        end_date = (datetime.now() - timedelta(days = 7)).strftime(time_format)
        
        pool = multiprocessing.Pool()
        args = [(symbol, start_date, end_date, time_format, interval) for symbol in symbols]
        backtest_results = pool.starmap(self.backtest, args)
        pool.close()
        pool.join()

        # df.apply(lambda row: self.backtest(symbol="NSE:"+row['Symbol']+""),axis=1)
        # df.apply(lambda row: self.backtest(symbol="NSE:"+row['Symbol']+""),axis=1)
        # df['Symbol'] = df['Symbol']+'.NS'

        backtest_results = [x for x in backtest_results if x is not None]
        backtest_results = sorted(backtest_results, key=lambda result: result['value'], reverse=True)[:5]
        print("Top 5 backtest_results")
        print(backtest_results)

        # ---------------------- forward testing ---------------------------#
        start_date = (datetime.now() - timedelta(days = 7)).strftime(time_format)
        end_date = (datetime.now() - timedelta(days = 0)).strftime(time_format)

        pool = multiprocessing.Pool()
        top5StockSymbols = [result['symbol'] for result in backtest_results]
        args = [(symbol, start_date, end_date, time_format, interval) for symbol in top5StockSymbols]
        forwardtest_results = pool.starmap(self.backtest, args)
        pool.close()
        pool.join()

        print('forward test results')
        print(forwardtest_results)
        pass

    def __init__(self) -> None:

        # df = pd.read_csv(r'./data/nifty100.csv')
        df = pd.read_csv(r'./data/volitileStocks.csv')
        df['Symbol'] = 'NSE:'+ df['Symbol']
        symbols = df['Symbol'].to_list()

        time_format = "%Y-%m-%d %H:%M:%S"
        interval = ["5minute"]
        self.multiprocessedBacktest(symbols, time_format, interval)

        # start_date = (datetime.now() - timedelta(days = 30)).strftime(time_format)
        # end_date = (datetime.now() - timedelta(days = 0)).strftime(time_format)
        # self.backtest(symbol="NSE:NIFTY BANK")
        # self.backtest(symbol="NFO:NIFTY23FEB16500CE")
        # self.backtest("NSE:BOSCHLTD", start_date, end_date, time_format, interval)
        # self.backtest("NSE:ADANIGREEN", start_date, end_date, time_format, interval)

        #---- for yahoo finance data
        # NSE index
        # self.backtest(symbol="^NSEI")
        # self.backtest(symbol="HDFC.NS")
