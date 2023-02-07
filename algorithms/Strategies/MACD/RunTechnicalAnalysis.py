# Should be used for intraday trading.
# Hence has a shorter time interval of weeks in the data used.

from datetime import datetime, timedelta

import backtrader as bt
from algorithms.Strategies.MACD.KiteConnect import KiteConnectData
from algorithms.Strategies.MACD.Strategy import Strategy

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
        days = 5
        print(f"Backtesting: using {days} days old data")
    #---------------------Kite Data -------------------------#

        start_date = (datetime.now() - timedelta(days = days)).strftime(time_format)
        end_date = (datetime.now() - timedelta(days = 0)).strftime(time_format)

        kiteConnectData = KiteConnectData(time_format, symbol, fromDate=start_date, toDate=end_date, interval = ["5minute"])

        cerebro.adddata(kiteConnectData.data)
    #-------------------- Kite data end --------------------------#

        # # Define the optimization parameters and ranges
        cerebro.addstrategy(Strategy)
        # cerebro.optstrategy(Strategy)
        # cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name="TAnalyzer")


        print('Backtesting: Starting portfolio Value: %.2f' % cerebro.broker.getvalue())

        cerebro.run()
        # cerebro.plot(iplot=True, volume=False, style='bar', rows=2, cols=1, name=['macd'])
        cerebro.plot()

        print('Backtesting: Final portfolio Value: %.2f' % cerebro.broker.getvalue())
    

    def __init__(self) -> None:
        self.backtest(symbol="NSE:NIFTY BANK")
        # self.backtest(symbol="NFO:NIFTY23FEB16500CE")
        # self.backtest(symbol="NSE:ADANIGREEN")
        # self.backtest(symbol="NSE:TCS")
        # self.backtest(symbol="NSE:NIFTYBEES")

        #---- for yahoo finance data
        # NSE index
        # self.backtest(symbol="^NSEI")
        # self.backtest(symbol="HDFC.NS")
