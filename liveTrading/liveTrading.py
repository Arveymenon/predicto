import backtrader as bt

# from DataConnect.KiteConnectData import KiteConnectData
from DataConnect.KiteLiveDataConnect import LiveDataFeed

from Indicators.SuperTrend import SuperTrend
from pandas import DataFrame

from backtesting.commission import ZerodhaCommission
from broker.ZerodhaBroker import ZerodhaBroker

from analyzers.commissions import CommissionsAnalyzer
from analyzers.totalValue import TotalValueAnalyzer

def liveTrading(
        symbol, 
        exchange,
        interval,
        Strategy,
        initialInvestment,
        plot = False,
    ):

    # Live Trading
    print("live trading: started for "+ symbol)
    cerebro = bt.Cerebro()

    cerebro.setbroker(ZerodhaBroker())
    cerebro.broker.setcash(cash = initialInvestment)
    cerebro.broker.setcommission(commission=0.0)  # Disable default commission
    cerebro.broker.addcommissioninfo(ZerodhaCommission())
    
    #---------------------Kite Data -------------------------#
    kiteConnectData = LiveDataFeed(symbol, exchange, interval = interval)
    try:
        if kiteConnectData.success:
            
            for data in kiteConnectData.datas:
                cerebro.adddata(data)

        #-------------------- Kite data end --------------------------#

            print('Live Trading: Starting portfolio Value: %.2f' % cerebro.broker.getvalue())

            cerebro.addstrategy(Strategy)
            cerebro.run()

            if(plot):
                # cerebro.plot(iplot=True, volume=False, style='bar', rows=2, cols=1, name=['macd'])
                cerebro.plot(style='candlestick', subplot=False)


            print('Live trading: Final portfolio Value: %.2f' % cerebro.broker.getvalue())
            return {"symbol": symbol, "value": cerebro.broker.getvalue()}


    except Exception as e:
        print(f"Error live trading: {e}")
        return {"symbol": symbol, "value": initialInvestment}