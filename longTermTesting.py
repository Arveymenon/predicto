import os
import shutil
from configuration import config as baseConfig
from flask import Flask

from kite_connect.main import KiteConnect
from algorithms.Strategies.MACD.RunTechnicalAnalysis import RunTechnicalAnalysis
from utilities.isHoliday import isHoliday

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
    config["shortlisting"]["interval"]["start_datetime"] = (start_date - timedelta(days = 30)).strftime("%Y-%m-%d 09:00:00")
    config["shortlisting"]["interval"]["end_datetime"] = (start_date  - timedelta(days = 2)).strftime("%Y-%m-%d 09:00:00")

    config["backtesting"]["interval"]["start_datetime"] = (start_date  - timedelta(days = 2)).strftime("%Y-%m-%d 09:00:00")
    config["backtesting"]["interval"]["end_datetime"] = (start_date  - timedelta(days = 0)).strftime("%Y-%m-%d 16:00:00")

    return config

if __name__ == "__main__":

    # init kite connect
    kite = KiteConnect().kite
    
    # backtrading init
    # runTechnicalAnalysis = RunTechnicalAnalysis()       

    if os.path.exists(baseConfig["tempFilesPath"]):
        shutil.rmtree(baseConfig["tempFilesPath"])
        
    os.mkdir(baseConfig["tempFilesPath"])

    # start_date = datetime(2022, 3, 1, 18, 38, 36, 73208)
    start_date = datetime.now() - timedelta(days = 730)
    end_date = datetime.now() - timedelta(days = 1)
    d = end_date - start_date
    deletable_array = []
    
    config = baseConfig
    count = 0
    for i in range(0, d.days + 1, 2):
        current_date = start_date + timedelta(days = i)

        if not isHoliday(current_date):
            config = getConfig(config, current_date)

            if(config["shortlisting"]["isActive"]):
                shortlist = Shortlist(config)

            if(not config["shortlisting"]["isActive"] or len(shortlist.shortlisted_stocks) > 0):
                backtesting = Backtesting(config)
                count+=1
                config["initialInvestment"] = backtesting.total
                deletable_array.append(backtesting.total)
        
        print(count)
    # setting this will
    # cerebro.run(broker=kite)


# For Reference for Yahoo Finance
# valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
# valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo