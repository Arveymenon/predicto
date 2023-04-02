import pandas as pd
from backtesting import multiprocessedBacktesting
# from algorithms.Strategies.MovingAverageCrossover.Strategy import Strategy
from algorithms.Strategies.FiveEMA.Strategy import Strategy
from algorithms.Strategies.CGPTGenerated import CGPTGeneratedStrategy
from datetime import datetime, timedelta


from backtesting.backtest import backtest
# from configuration import config




class Backtesting:

    def __init__(self ,config) -> None:
        shortlist = config["shortlisting"]["strategyName"]
        self.dataSetFileName = config["inputFile"]
        self.algo = config["backtesting"]["strategyName"]

        df = pd.read_csv(r'./data/responseData/shortlist/'+shortlist+"."+self.dataSetFileName+'.csv')
        # df['Symbol'] = 'NSE:'+ df['Symbol']
        df['Symbol'] = config['exchange']+":"+df['Symbol']
        symbols = df['Symbol'].to_list()


        datetime_format = "%Y-%m-%d %H:%M:%S"

        backtestTimeFrame = [
            config["backtesting"]["interval"]["start_datetime"],
            config["backtesting"]["interval"]["end_datetime"]
        ]

        optimization_params = config["backtesting"]["optimization"]

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
        # comment out for multiprocessing (Cannot be used with optStrategy) # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

        if(not optimization_params):
            self.total = multiprocessedBacktesting \
                            .multiProcessedBacktest(
                                symbols,
                                backtestTimeFrame,
                                datetime_format,
                                self.generateResponse
                            )
        else:
            results = []
            budget = config["initialInvestment"]/len(symbols)
            # #### TODO: replace config["initialInvestment"] with budget in backtest()
            for symbol in symbols :
                back_tested_data = backtest(
                        symbol,
                        backtestTimeFrame[0], backtestTimeFrame[1], datetime_format, config["backtesting"]["interval"]["intervals"],
                        config["backtesting"]["strategy"],
                        budget,
                        config["backtesting"]["plot"],
                        True
                    )
                
                if back_tested_data != None and len(back_tested_data) :
                    results.append([back_tested_data['symbol'], back_tested_data['value']])

            self.generateResponse(results)

    def generateResponse(self, results):
        df = pd.DataFrame(results, columns = ["symbol", "value"])

        df = df.sort_values(by='value', ascending=False)
        print(df)
        self.total = df["value"].sum()
        print(self.total)
        df.to_csv("./data/responseData/backtest/"+self.dataSetFileName+"."+self.algo+".csv")


