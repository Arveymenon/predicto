from flask import Flask

from generateData import GenerateData
from runTechnicalAnalyisis import RunTechnicalAnalysis

# from test import MyStrategy

app = Flask(__name__)


@app.route('/')
def hello():
    # 
    return 'Hey Guys!'



if __name__ == "__main__":
    data = GenerateData()
    # historicalData = data.historicalNSEData("1m", "1d")

    runTechnicalAnalysis = RunTechnicalAnalysis(data)