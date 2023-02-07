import os
import pandas as pd
import yfinance as yf

import plotly.express as px
import plotly.graph_objects as go

from typing import List

import calendar
from datetime import datetime

class GenerateData():
    # Define the symbol and the interval (1 days)
    interval = "1d"  #1 days interval
    period="1y" # 1 years period

    # data = pd.DataFrame()
    suggestedBuy = []

    def plotLine(self, df, x_axis: str, y_axis: str, dimensions):
        print("GenerateData:plotLine function started")
        df.to_csv("data/temp/ACC.NShistorical_data_moving_avg.csv")
        
        fig = go.Figure()
        for dimension in dimensions:
            fig.add_trace(go.Scatter(x=df[x_axis], y=df[dimension], name=dimension))

        # Set the title and labels
        fig.update_layout(title='ACC Stock Price', 
                        xaxis_title= x_axis,
                        yaxis_title= y_axis)

        fig.show()

    def historicalNSEData(self, interval = interval, period = period, symbol = None):
        # get data for which stock
        df = pd.read_csv(r'./data/nifty100.csv')
        df['Symbol'] = df['Symbol']+'.NS'
        
        if(symbol):
            yf.download(symbol, period=period, interval=interval).to_csv("./data/NSE100StockData/"+symbol+".historical_data.csv")
        else:
            for symbol in df['Symbol']:
                yf.download(symbol, period=period, interval=interval).to_csv("./data/NSE100StockData/"+symbol+".historical_data.csv")



    def createData(self, symbol, period = period, interval = interval, startDate= None, endDate= None):
        temp_file_name =  "data/temp/"+ datetime.now().isoformat() +"-"+symbol+".historical_data.csv"
        if(startDate and endDate):
            yf.download(symbol, start= startDate, end=endDate, interval = interval).to_csv(
                   "./"+temp_file_name
                )
        else:
            yf.download(symbol, period = period, interval = interval).to_csv(
                    "./"+temp_file_name
                )

        return "/Users/arulvinayak/Desktop/Projects/stockMarketPredictor/predicto/"+ temp_file_name

    # def completeHistoricalNSEData(self):
        
    #     start = pd.to_datetime('2001-01-01')
    #     end = pd.to_datetime('2021-01-01')

        
    #     df = pd.read_csv(r'./data/nifty100.csv')
    #     df['Symbol'] = df['Symbol']+'.NS'
    #     os.makedirs('./data/NSE100StockData')

    #     for symbol in df['Symbol']:    
    #         for year in range(2001, 2022):
    #             path = './data/NSE100StockData/ %i'%year
    #             if not os.path.exists(path):
    #                 os.makedirs(path)
    #             for month in range(1, 13):
    #                 path = './data/NSE100StockData/'+str(year)+"/"+str(month)
    #                 if not os.path.exists(path):
    #                     os.makedirs(path)
    #                 input_dt = datetime(year, month, 1)
                    
    #                 res = calendar.monthrange(input_dt.year, input_dt.month)
    #                 day = res[1]

    #                 start = str(year)+"-"+str(month)+"-01"
    #                 end = str(year)+"-"+str(month) +"-"+ str(day)
    #                 yf.download(symbol, start= start, end=end).to_csv(
    #                         "./data/NSE100StockData/"+str(year)+"/"+str(month)+"/"+symbol+".historical_data.csv"
    #                     )

    def __init__(self) -> None:
        pass