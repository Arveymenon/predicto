import os
import shutil
from configuration import config as baseConfig, getConfig
from flask import Flask
from algorithms.Strategies.MACD.RunTechnicalAnalysis import RunTechnicalAnalysis

from kite_connect.main import KiteConnect

from backtesting.main import Backtesting
from shortlisting.main import Shortlist
from datetime import datetime, date, timedelta
import multiprocessing as mp

app = Flask(__name__)


@app.route('/')
def hello():
    # 
    return 'Hey Guys!'

def getConfig(config, start_date):
    config["shortlisting"]["interval"]["start_datetime"] = (start_date - timedelta(days = 60)).strftime("%Y-%m-%d 09:15:00")
    config["shortlisting"]["interval"]["end_datetime"] = (start_date  - timedelta(days = 2)).strftime("%Y-%m-%d 15:30:00")

    config["backtesting"]["interval"]["start_datetime"] = (start_date  - timedelta(days = 1)).strftime("%Y-%m-%d 09:15:00")
    config["backtesting"]["interval"]["end_datetime"] = (start_date  - timedelta(days = 0)).strftime("%Y-%m-%d 09:30:00")

    return config

if __name__ == "__main__":

    # init kite connect
    kite = KiteConnect().kite
    
    # backtrading init
    # runTechnicalAnalysis = RunTechnicalAnalysis()       

    if os.path.exists(baseConfig["temp_files_path"]):
        shutil.rmtree(baseConfig["temp_files_path"])
        
    os.mkdir(baseConfig["temp_files_path"])

    start_date = datetime(2022, 11, 11, 18, 38, 36, 73208)
    end_date = datetime(2023, 3, 3)
    d = end_date - start_date

    # new_config = []
    # new_config.append(baseConfig)
    config = baseConfig
    for i in range(d.days + 1):
        start_date += timedelta(days = i)

        config = getConfig(config, start_date)

        Shortlist(config)

        # if(len(shortlist.shortlisted_stocks) > 0):
        #     backtesting = Backtesting(new_config)
        #     new_config[i+1] = getConfig(new_config[i], day)
        #     new_config["initialInvestment"] = backtesting.total


    # setting this will
    # cerebro.run(broker=kite)


# For Reference for Yahoo Finance
# valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
# valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo