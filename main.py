from flask import Flask
from algorithms.Strategies.FiveEMA.RunTechnicalAnalysis import RunTechnicalAnalysis5EMA

from generateData import GenerateData

# from test import MyStrategy

app = Flask(__name__)


@app.route('/')
def hello():
    # 
    return 'Hey Guys!'



if __name__ == "__main__":
    data = GenerateData()

     # valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
     # valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo

    # historicalData = data.historicalNSEData("1m", "1d")
    # historicalData = data.historicalNSEData("1d", "2y","WIPRO.NS")
    # historicalData = data.completeHistoricalNSEData()
    # historicalData = data.historicalNSEData("1m", "5d","WIPRO.NS")

    runTechnicalAnalysis = RunTechnicalAnalysis5EMA(data)