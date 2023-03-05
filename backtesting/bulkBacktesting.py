import backtrader as bt

from DataConnect.KiteConnect import KiteConnectData
from backtesting.commission import ZerodhaCommission
from pandas import DataFrame

INITIAL_INVESTMENT = 10000.0

def bulkBacktest(
        symbols,
        start_date, end_date, datetime_format, interval,
        Strategy,
        plot = False, 
        optimization_params = None, 
        initialInvestment=INITIAL_INVESTMENT
    ):

    # Backtesting
    print("Backtesting: started for "+ symbols)
    cerebro = bt.Cerebro()
    cerebro.broker.setcash(initialInvestment)

    cerebro.broker.setcommission(commission=0.0)  # Disable default commission
    cerebro.broker.addcommissioninfo(ZerodhaCommission())

    
    #---------------------Kite Data -------------------------#
    for symbol in symbols: 
        kiteConnectData = KiteConnectData(datetime_format, symbol, fromDate=start_date, toDate=end_date, interval = interval)
        for data in kiteConnectData.datas:
            cerebro.adddata(data)

            # cerebro.adddata(kiteConnectData.data2)

    #-------------------- Kite data end --------------------------#

    # # Define the optimization parameters and ranges
    cerebro.addstrategy(Strategy)
    
    print('Backtesting: Starting portfolio Value: %.2f' % cerebro.broker.getvalue())
    cerebro.run()

    if(plot):
        # cerebro.plot(iplot=True, volume=False, style='bar', rows=2, cols=1, name=['macd'])
        cerebro.plot(iplot=True, volume=False, style='candlestick')
        # cerebro.plot()

    print('Backtesting: Final portfolio Value: %.2f' % cerebro.broker.getvalue())

    return {"symbol": symbol, "value": cerebro.broker.getvalue()}



def getIdealParams(results):

    opt_results = []
    # print(results[0][0])

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

    print(df)

    # fast = df['fast'].values
    # slow = df['slow'].values
    # print(fast, slow)

    return df