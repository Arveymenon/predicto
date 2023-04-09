import os
import shutil
import sys

import rel
import websocket
import json

from flask import Flask
import pandas as pd
from datetime import datetime

from kite_connect.main import KiteConnect
from algorithms.Strategies.MACD.RunTechnicalAnalysis import RunTechnicalAnalysis

from backtesting.main import Backtesting
from shortlisting.main import Shortlist
from liveTrading.liveTrading import liveTrading

from configuration import config


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

    if config["liveTrade"]:
        confirmation = input("Are you dead sure you want to start live trading? [Y/N]")
        if(confirmation != 'Y' and confirmation != 'y'):
            sys.exit()
        else:
            # TODO: 
            #  1. OOPS to be implemented.
            #  2. dynamic data implemenation
            liveTrading(
                "SAPPHIRE", 
                "NSE",
                config["backtesting"]["interval"]["intervals"],
                config["backtesting"]["strategy"],
                config["initialInvestment"])
            pass

    else:
        if(config["shortlisting"]["isActive"]):
            Shortlist(config)

        if(config["backtesting"]["isActive"]):
            Backtesting(config)
        pass
