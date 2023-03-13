import pandas as pd
import numpy as np
# df = pd.read_csv(r'./data/nifty100.csv')



class MovingAverage():

    __short_term_ema, __long_term_ema, __Close = 'short_term_ema', 'long_term_ema', 'Close'
    
    def calculate(self):
        # Load the stock data into a DataFrame
        
        # TODO: NEEDS TO BE UPDATED TO WORK FOR ALL HISTORICAL DATA
        # df = pd.read_csv()
        df = pd.read_csv(self.__data)

        df[self.__short_term_ema] = df['Close'].ewm(span=7).mean()
        df[self.__long_term_ema] = df['Close'].ewm(span=20).mean()

        # Create a new column to hold the EMA crossover signals
        df['Signal'] = np.where(df['short_term_ema'] > df['long_term_ema'], 1, 0)

        # Create a new column to hold the buy and sell signals
        df['Buy_Signal'] = np.where((df['Signal'] == 1) & (df['Signal'].shift(1) == 0), 1, 0)
        df['Sell_Signal'] = np.where((df['Signal'] == 0) & (df['Signal'].shift(1) == 1), 1, 0)

        return df

    def plotCols(self, data):
        self.__data = data
        return [self.__short_term_ema, self.__long_term_ema, self.__Close]