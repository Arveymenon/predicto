import os
import shutil
from configuration import config
from flask import Flask
import pandas as pd
from datetime import datetime

from kite_connect.main import KiteConnect
from algorithms.Strategies.MACD.RunTechnicalAnalysis import RunTechnicalAnalysis

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

    # get holding using kite.holdings()
    
    # backtrading init
    # runTechnicalAnalysis = RunTechnicalAnalysis()
    if os.path.exists(config["tempFilesPath"]):
        shutil.rmtree(config["tempFilesPath"])
        
    os.mkdir(config["tempFilesPath"])
    
    if(config["shortlisting"]["isActive"]):
        Shortlist(config)

    if(config["backtesting"]["isActive"]):
        Backtesting(config)