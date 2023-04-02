from backtesting.backtest import backtest
import multiprocessing
import pandas as pd
from configuration import config, BudgetDistribution

shortlist = config["shortlisting"]["strategyName"]
dataSetFileName = config["inputFile"]
algo = config["backtesting"]["strategyName"]


def multiProcessedBacktest(symbols, 
            backtestTimeFrame,
            datetime_format,
            generateResponse
            ):
         # ---------------------- Back testing ---------------------------#
        
            if(len(symbols)):

                if(config["budgetDistribution"] == BudgetDistribution.none):
                    budget = config["initialInvestment"]
                else:
                    budget = config["initialInvestment"]/len(symbols)

                pool = multiprocessing.Pool()
                results = []

                args = [(
                        symbol,
                        backtestTimeFrame[0], backtestTimeFrame[1], datetime_format, 
                        config["backtesting"]["interval"]["intervals"],
                        config["backtesting"]["strategy"],
                        budget,
                        config["backtesting"]["plot"],
                        None) for symbol in symbols]
                backtest_results = pool.starmap(backtest, args)
                pool.close()
                pool.join()

                # backtest_results = [x for x in backtest_results if x is not None]
                # backtest_results = sorted(backtest_results, key=lambda result: result['value'], reverse=True)[:5]

                if(len(backtest_results) > 0):
                    for back_tested_data in backtest_results:
                        if back_tested_data != None and len(back_tested_data) :
                            results.append([back_tested_data['symbol'], back_tested_data['value']])
                else:
                     return config["initialInvestment"]


                generateResponse(results)
