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
        dataSetFileName = config["input_file"]
        algo = config["backtesting"]["strategyName"]

        df = pd.read_csv(r'./data/responseData/shortlist/'+shortlist+"."+dataSetFileName+'.csv')
        df['Symbol'] = 'NSE:'+ df['Symbol']
        symbols = df['Symbol'].to_list()
        # symbols = ["NSE:PATANJALI-BE"]


        datetime_format = "%Y-%m-%d %H:%M:%S"
        interval = ["5minute", "15minute"]

        backtestTimeFrame = [
            config["backtesting"]["interval"]["start_datetime"],
            config["backtesting"]["interval"]["end_datetime"]
        ]

        forwardTimeFrame = []

        optimization_params = None
        # optimization_params = {
        #     # 'test': True
        # }
        # "fast": range(5,10),
        # "slow": range(15,30)

        # multiprocessedBacktesting \
        #                 .multiProcessedBacktest(
        #                     symbols,
        #                     datetime_format, interval, 
        #                     Strategy, backtestTimeFrame,True, forwardTimeFrame,
        #                     plot = False, 
        #                     optimization_params=optimization_params
        #                 )

        if(optimization_params == None):
            # back_tested_data = backtest(
            #         symbol,
            #         backtestTimeFrame[0], backtestTimeFrame[1], datetime_format, interval, 
            #         Strategy,
            #         plot=True,
            #         optimization_params=None
            #     )
            results = []
            budget = config["initialInvestment"]/len(symbols)
            for symbol in symbols :
                back_tested_data = backtest(
                        symbol,
                        backtestTimeFrame[0], backtestTimeFrame[1], datetime_format, interval,
                        config["backtesting"]["strategy"],
                        budget,
                        plot=config["backtesting"]["plot"],
                        optimization_params=None
                    )
                results.append([back_tested_data['symbol'], back_tested_data['value']])
                
            df = pd.DataFrame(results, columns = ["symbol", "value"])

            df = df.sort_values(by='value', ascending=False)
            print(df)
            self.total = df["value"].sum()
            print(self.total)
            df.to_csv("./data/responseData/backtest/"+dataSetFileName+"."+algo+".csv")

        else:
            # "fast", "slow", "stop_loss", "take_profit",
            optimum_params = pd.DataFrame([], columns = [
                                                "symbol", "net_profit", 'won_total', 'lost_total'])
            for symbol in symbols:
                back_tested_data = backtest(
                    symbol,
                    backtestTimeFrame[0], backtestTimeFrame[1], datetime_format, interval, 
                    config["backtesting"]["interval"]["strategy"],
                    plot=False,
                    optimization_params=optimization_params
                )

                if(not back_tested_data.empty):
                    back_tested_data["symbol"] = symbol

                    # If only backtesting is required
                    # optimum_params = optimum_params.append(back_tested_data.iloc[0],ignore_index=True)

                    # forward testing 
                    # "fast": back_tested_data["fast"],
                    # "slow": back_tested_data["slow"]
                    forward_test_optimization_param = {
                        'test': True
                    }

                    forward_tested_data = backtest(
                        symbol,
                        forwardTimeFrame[0], forwardTimeFrame[1], datetime_format, interval, 
                        Strategy,
                        plot=True,
                        optimization_params=forward_test_optimization_param
                    )

                    if(not forward_tested_data.empty):
                        # optimum_params.loc[symbol] = forward_tested_data
                        forward_tested_data["symbol"] = symbol
                        optimum_params = optimum_params.append(forward_tested_data.iloc[0],ignore_index=True)


            optimum_params = optimum_params.sort_values(by='net_profit', ascending=False)
            optimum_params.to_csv("./data/responseData/MovingAverageCrossover."+dataSetFileName+".csv")




