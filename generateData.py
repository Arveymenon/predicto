import pandas as pd
import yfinance as yf

import plotly.express as px
import plotly.graph_objects as go

from typing import List

class GenerateData():
    # Define the symbol and the interval (1 days)
    interval = "1d"  #1 days interval
    period="1y" # 5 years period

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

    def historicalNSEData(self, interval = interval, period = period):
        # get data for which stock
        df = pd.read_csv(r'./data/nifty100.csv')
        df['Symbol'] = df['Symbol']+'.NS'
        
        for symbol in df['Symbol']:
            yf.download(symbol, period=period, interval=interval).to_csv("./data/NSE100StockData/"+symbol+"historical_data.csv")

    def __init__(self) -> None:
        pass