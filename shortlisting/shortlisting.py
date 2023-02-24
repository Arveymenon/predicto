import backtrader as bt\

from DataConnect.KiteConnect import KiteConnectData

shortlisted_stocks = list()

def shortlist(
        symbol,
        start_date, end_date, datetime_format, interval,
        Strategy,
        plot = False
    ):

    # Backtesting
    print('Shortlisting test for: %s' % symbol)
    cerebro = bt.Cerebro()
    #---------------------Kite Data -------------------------#
    kiteConnectData = KiteConnectData(datetime_format, symbol, fromDate=start_date, toDate=end_date, interval = interval)

    if kiteConnectData.success:

        for data in kiteConnectData.datas:
            cerebro.adddata(data)

    #-------------------- Kite data end --------------------------#
        # strategy = Strategy()
        # cerebro.addstrategy(Strategy)
        cerebro.addstrategy(Strategy, symbol=symbol)
        
        cerebro.run()

        if(plot):
            # cerebro.plot(iplot=True, volume=False, style='bar', rows=2, cols=1, name=['strategy_name'])
            cerebro.plot(iplot=True, volume=False, style='candlestick')

        return {"symbol": symbol, "isInsideDay": False}