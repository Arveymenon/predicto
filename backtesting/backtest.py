import backtrader as bt

from DataConnect.KiteConnect import KiteConnectData
from backtesting.commission import ZerodhaCommission
from Indicators.SuperTrend import SuperTrend
from pandas import DataFrame

from Indicators.VWAP import VWAP

def backtest(
        symbol, 
        start_date, end_date, datetime_format, interval,
        Strategy,
        initialInvestment,
        plot = False, 
        optimization_params = None, 
    ):

    # Backtesting
    print("Backtesting: started for "+ symbol)
    cerebro = bt.Cerebro()
    cerebro.broker.setcash(initialInvestment)

    cerebro.broker.setcommission(commission=0.0)  # Disable default commission
    cerebro.broker.addcommissioninfo(ZerodhaCommission())

    
    #---------------------Kite Data -------------------------#
    kiteConnectData = KiteConnectData(datetime_format, symbol, fromDate=start_date, toDate=end_date, interval = interval)
    # try:
    if kiteConnectData.success:

        
        for data in kiteConnectData.datas:
            cerebro.adddata(data)
            # cerebro.adddata(kiteConnectData.data2)

    #-------------------- Kite data end --------------------------#

        # # Define the optimization parameters and ranges
        if optimization_params == None:
            cerebro.addstrategy(Strategy)
            
            print('Backtesting: Starting portfolio Value: %.2f' % cerebro.broker.getvalue())
            cerebro.run()

            if(plot):
                # cerebro.plot(iplot=True, volume=False, style='bar', rows=2, cols=1, name=['macd'])
                cerebro.plot(style='candlestick', subplot=False)

            print('Backtesting: Final portfolio Value: %.2f' % cerebro.broker.getvalue())

            return {"symbol": symbol, "value": cerebro.broker.getvalue()}

        else:
            cerebro.optstrategy(Strategy, **optimization_params)
            cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name="TAnalyzer")
            results = cerebro.run()
            return getIdealParams(results)
    # except:
    #     print("Error back testing")


def getIdealParams(results):

    opt_results = []

    # int(x[0].params.fast),
    # int(x[0].params.slow),
    # x[0].params.stop_loss,
    # x[0].params.take_profit,
    for x in results:
        opt_results.append([
            x[0].analyzers.TAnalyzer.get_analysis()['pnl']['net']['total'] if 'pnl' in x[0].analyzers.TAnalyzer.get_analysis() else 0,
            x[0].analyzers.TAnalyzer.get_analysis()['won']['pnl']['total'] if 'won' in x[0].analyzers.TAnalyzer.get_analysis() else 0,
            x[0].analyzers.TAnalyzer.get_analysis()['lost']['pnl']['total'] if 'lost' in x[0].analyzers.TAnalyzer.get_analysis() else 0
        ])

    # "fast", "slow", "stop_loss", "take_profit", 
    df = DataFrame(opt_results, columns = ["net_profit", 'won_total', 'lost_total'])
    df = df \
            .sort_values(by='net_profit', ascending=False).head(10)


    # fast = df['fast'].values
    # slow = df['slow'].values

    return df