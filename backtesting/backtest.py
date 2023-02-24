import backtrader as bt
from algorithms.Strategies.MACD.KiteConnect import KiteConnectData

INITIAL_INVESTMENT = 100000
COMMISSION = 0.002

def backtest(symbol, start_date, end_date, datetime_format, interval, strategy, initialInvestment=INITIAL_INVESTMENT):
    # Backtesting 
    print("Backtesting: started")
    cerebro = bt.Cerebro()
    cerebro.broker.setcash(initialInvestment)
    cerebro.broker.setcommission(commission=COMMISSION)
    
#---------------------Kite Data -------------------------#
    kiteConnectData = KiteConnectData(datetime_format, symbol, fromDate=start_date, toDate=end_date, interval = interval)

    if kiteConnectData.success:

        cerebro.adddata(kiteConnectData.data)
        #-------------------- Kite data end --------------------------#

        # # Define the optimization parameters and ranges
        cerebro.addstrategy(strategy)
        # cerebro.optstrategy(Strategy)
        # cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name="TAnalyzer")


        print('Backtesting: Starting portfolio Value: %.2f' % cerebro.broker.getvalue())

        cerebro.run()
        # cerebro.plot(iplot=True, volume=False, style='bar', rows=2, cols=1, name=['macd'])
        # cerebro.plot(iplot=True, volume=False, style='bar')
        # cerebro.plot()

        print('Backtesting: Final portfolio Value: %.2f' % cerebro.broker.getvalue())

        return {"symbol": symbol, "value": cerebro.broker.getvalue()}