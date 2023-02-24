from backtesting.backtest import backtest
import multiprocessing

def multiProcessedBacktest(
            symbols, 
            datetime_format, interval, strategy, backtestTimeFrame, 
            forwardTest = False, forwardTimeFrame = [],
            plot = False, 
            optimization_params = None
            ):
         # ---------------------- Back testing ---------------------------#
        
        if(optimization_params == None):

            pool = multiprocessing.Pool()
            args = [(symbol, backtestTimeFrame[0], backtestTimeFrame[1], datetime_format, interval, strategy) for symbol in symbols]
            backtest_results = pool.starmap(backtest, args)
            pool.close()
            pool.join()

            backtest_results = [x for x in backtest_results if x is not None]
            backtest_results = sorted(backtest_results, key=lambda result: result['value'], reverse=True)[:5]
            print("Top 5 backtest_results")
            print(backtest_results)

            # ---------------------- forward testing ---------------------------#
            if(forwardTest):

                pool = multiprocessing.Pool()
                top5StockSymbols = [result['symbol'] for result in backtest_results]
                args = [(symbol, forwardTimeFrame[0], forwardTimeFrame[1], datetime_format, interval, strategy) for symbol in top5StockSymbols]
                forwardtest_results = pool.starmap(backtest, args)
                pool.close()
                pool.join()

                print('forward test results')
                print(forwardtest_results)

        else:
            pool = multiprocessing.Pool()
            args = [(
                    symbol, 
                    backtestTimeFrame[0], backtestTimeFrame[1], datetime_format, interval,
                    strategy,
                    plot,
                    optimization_params) for symbol in symbols]
            
            backtest_results = pool.starmap(backtest, args)
            pool.close()
            pool.join()

            print(backtest_results)
            # if(forwardTest):
            #     optimization_params
            #     pool = multiprocessing.Pool()
            #     top5StockSymbols = [result['symbol'] for result in backtest_results]
            #     args = [(
            #         symbol, 
            #         forwardTimeFrame[0], forwardTimeFrame[1], datetime_format, interval,
            #         strategy,
            #         plot,
            #         optimization_params) for symbol in symbols]
            #     forwardtest_results = pool.starmap(backtest, args)
            #     pool.close()
            #     pool.join()

            #     print('forward test results')
            #     print(forwardtest_results)