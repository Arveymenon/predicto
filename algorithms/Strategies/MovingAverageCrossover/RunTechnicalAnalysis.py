from datetime import datetime, timedelta

import numpy as np
from pandas import DataFrame
import yfinance as yf

from algorithms.Analyzers.profit import ProfitAnalyzer
from algorithms.Strategies.MovingAverageCrossover.Strategy import Strategy
# from algorithms.moving_average_crossover import MovingAverage
# from algorithms.Strategies.testStrategy import TestStrategy

import backtrader as bt

from generateData import GenerateData


INITIAL_INVESTMENT = 100000

class RunTechnicalAnalysis():
    
    def backtestMovingAverage(self, symbol, initialInvestment=INITIAL_INVESTMENT):
        # Backtesting 
        print("Backtesting: started")
        cerebro = bt.Cerebro()
        cerebro.broker.setcash(initialInvestment)
        print("Backtesting: using 2 years old data")

        start_date = (datetime.now() - timedelta(days=365 * 10)).strftime("%Y-%m-%d")
        end_date = (datetime.now() - timedelta(days=365 * 1)).strftime("%Y-%m-%d")

        generateData = GenerateData()
        dataname = generateData.createData(symbol, startDate=start_date, endDate=end_date)

        data = bt.feeds.YahooFinanceCSVData(
            dataname = dataname,
            reverse=False
        )

        cerebro.adddata(data)
        cerebro.adddata(data)

        # Define the optimization parameters and ranges
        cerebro.addstrategy(Strategy)
        # cerebro.optstrategy(Strategy, fast = range(5, 20), slow =  range(20,40))
        # stop_loss= np.arange(0.01,0.05,0.01), take_profit=np.arange(0.02,0.10,0.01)

        cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name="TAnalyzer")

        print('Backtesting: Starting portfolio Value: %.2f' % cerebro.broker.getvalue())

        results = cerebro.run()
        
        suggested_df = self.getIdealParams(results)
        self.fast_ema = suggested_df['fast'].head(10).values
        self.slow_ema = suggested_df['slow'].head(10).values

        print('Backtesting: Final portfolio Value: %.2f' % cerebro.broker.getvalue())
        print("Backtesting: ended")

    def getIdealParams(self, results):

        # print(results[0][0].analyzers.TAnalyzer.get_analysis())

        opt_results = []

        for x in results:
            opt_results.append([
                int(x[0].params.fast),
                int(x[0].params.slow),
                x[0].params.stop_loss,
                x[0].params.take_profit,
                x[0].analyzers.TAnalyzer.get_analysis()['pnl']['gross']['total'] if 'pnl' in x[0].analyzers.TAnalyzer.get_analysis() else 0,
                x[0].analyzers.TAnalyzer.get_analysis()['won']['pnl']['total'] if 'won' in x[0].analyzers.TAnalyzer.get_analysis() else 0,
                x[0].analyzers.TAnalyzer.get_analysis()['lost']['pnl']['total'] if 'lost' in x[0].analyzers.TAnalyzer.get_analysis() else 0
            ])

        df = DataFrame(opt_results, columns = ["fast", "slow", "stop_loss", "take_profit", "gross_profit", 'won_total', 'lost_total'])
        df = df.sort_values(by='gross_profit', ascending=False)

        return df

    def forwardtestMovingAverage(self, symbol, initialInvestment=INITIAL_INVESTMENT):
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
        # self.backtestMovingAverage(symbol="LT.NS")
        self.backtestMovingAverage(symbol="LT.ADANIGREEN")
        
        # self.forwardtestMovingAverage(symbol="LT.NS")
        self.forwardtestMovingAverage(symbol="LT.ADANIGREEN")
        pass
