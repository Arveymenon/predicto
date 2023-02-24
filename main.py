import os
import shutil
from configuration import config
from flask import Flask
from algorithms.Strategies.MACD.RunTechnicalAnalysis import RunTechnicalAnalysis

from kite_connect.main import KiteConnect

from backtesting.main import Backtesting
from shortlisting.main import Shortlist

app = Flask(__name__)


@app.route('/')
def hello():
    # 
    return 'Hey Guys!'



if __name__ == "__main__":

    # init kite connect
    kite = KiteConnect().kite
    # print(kite.holdings())
    
    # backtrading init
    # runTechnicalAnalysis = RunTechnicalAnalysis()       
    print("If temporary path exists",os.path.exists(config["temp_files_path"]))
    if os.path.exists(config["temp_files_path"]):
        shutil.rmtree(config["temp_files_path"])
        
    os.mkdir(config["temp_files_path"])

    Shortlist()
    Backtesting()

    # setting this will 
    # cerebro.run(broker=kite)


# For Reference for Yahoo Finance
# valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
# valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo