from pandas import DataFrame
from algorithms.moving_average_crossover import MovingAverage

import backtrader as bt

INITIAL_INVESTMENT = 10000

class RunTechnicalAnalysis():

    def movingAverage(self):
        print("RunTechnicalAnalysis:movingAverage function called")
        emaCross = MovingAverage()
        return emaCross.calculate()

    def __init__(self, data: DataFrame) -> None:


        # self.data = data

        # data.plotLine(df, "Datetime", "Close", emaCross.plotCols())

        # print(df)
        self.movingAverage()

        cerebro = bt.Cerebro()
        cerebro.set_cash(INITIAL_INVESTMENT)

        print('Starting protfolio Value: %.2f' % cerebro.broker.getvalue())
        
        cerebro.run()

        print('Final protfolio Value: %.2f' % cerebro.broker.getvalue())

        pass
