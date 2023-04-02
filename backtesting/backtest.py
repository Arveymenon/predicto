import backtrader as bt

from DataConnect.KiteConnect import KiteConnectData
from backtesting.commission import ZerodhaCommission
from Indicators.SuperTrend import SuperTrend
from pandas import DataFrame

from analyzers.commissions import CommissionsAnalyzer
from analyzers.totalValue import TotalValueAnalyzer

def backtest(
        symbol, 
        start_date, end_date, datetime_format, interval,
        Strategy,
        initialInvestment,
        plot = False, 
        optimization_params = False, 
    ):

    # Backtesting
    print("Backtesting: started for "+ symbol)
    cerebro = bt.Cerebro()
    cerebro.broker.setcash(initialInvestment)

    cerebro.broker.setcommission(commission=0.0)  # Disable default commission
    cerebro.broker.addcommissioninfo(ZerodhaCommission())

    
    #---------------------Kite Data -------------------------#
    kiteConnectData = KiteConnectData(datetime_format, symbol, fromDate=start_date, toDate=end_date, interval = interval)
    try:
        if kiteConnectData.success:

            
            for data in kiteConnectData.datas:
                cerebro.adddata(data)

            

        #-------------------- Kite data end --------------------------#

            print('Backtesting: Starting portfolio Value: %.2f' % cerebro.broker.getvalue())

            # # Define the optimization parameters and ranges
            if optimization_params == False:
                cerebro.addstrategy(Strategy)
                cerebro.run()

            else:
                cerebro.optstrategy(Strategy)
                cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name="TAnalyzer")
                cerebro.addanalyzer(TotalValueAnalyzer, _name="TotalValueAnalyzer")
                cerebro.addanalyzer(CommissionsAnalyzer, _name="CommissionAnalyzer")
                

                results = cerebro.run()

            if(plot):
                # cerebro.plot(iplot=True, volume=False, style='bar', rows=2, cols=1, name=['macd'])
                cerebro.plot(style='candlestick', subplot=False)


            if(optimization_params == False):

                print('Backtesting: Final portfolio Value: %.2f' % cerebro.broker.getvalue())
                return {"symbol": symbol, "value": cerebro.broker.getvalue()}

            else:
                commission_analyzers = results[0][0].analyzers.CommissionAnalyzer
                total_value_analyzers = results[0][0].analyzers.TotalValueAnalyzer

                print(f"Commission paid: {commission_analyzers.total_commission:.2f}")
                print("Net profit: %s" %results[0][0].analyzers.TAnalyzer.get_analysis()["pnl"]["net"]["total"])
                print('Backtesting: Final portfolio Value: %i' % total_value_analyzers.total_value)
                
                return {"symbol": symbol, "value": total_value_analyzers.total_value}

    except Exception as e:
        print(f"Error back testing: {e}")
        return {"symbol": symbol, "value": initialInvestment}


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