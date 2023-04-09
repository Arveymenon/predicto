from datetime import datetime, timedelta

from algorithms.Strategies.Shortlisting.InsideDay.InsideDay import InsideDayStrategy
# from algorithms.Strategies.Shortlisting.Volitility import VolatilityStrategy
from algorithms.Strategies.Shortlisting.MMI import MMI

# from algorithms.Strategies.MACD.Strategy import Strategy
from algorithms.Strategies.FiveEMA.Strategy2 import Strategy2

from algorithms.Strategies.Supertrend import SupertrendStrategy
from algorithms.Strategies.VWAP import VWAPStrategy
from algorithms.Strategies.VWAPMACDSuperTrend import VWAPMACDSuperTrendStrategy

from enum import Enum
# class budgetDistribution(Enum):
#     linear = 0
#     none = 1
BudgetDistribution = Enum("BudgetDistribution", ["linear", "none"])

# backtesting will be done on {shortlisting.strategyName} + "." + {inputFile}
config = {
    "liveTrade": False,
    "initialInvestment": 100,
    "tempFilesPath": "./data/temp/",
    "inputFile": "nsesmallcap100",
    "exchange": "NSE",
    "budgetDistribution": BudgetDistribution.linear,
    "shortlisting": {
        "isActive": False,
        "interval": {
            "datetime_format": "%Y-%m-%d %H:%M:%S",
            "start_datetime": (datetime.now() - timedelta(days = 8)).strftime("%Y-%m-%d 09:00:00"),
            "end_datetime": (datetime.now() - timedelta(days = 6)).strftime("%Y-%m-%d 09:00:00"),
            "intervals": ["day"],
        },
        "plot": False,
        "strategyName": "InsideDay",
        "strategy": InsideDayStrategy
    },
    "backtesting": {
        "isActive": True,
        "interval": {
            "datetime_format": "%Y-%m-%d %H:%M:%S",
            "start_datetime": (datetime.now() - timedelta(days = 4)).strftime("%Y-%m-%d 09:00:00"),
            "end_datetime": (datetime.now() - timedelta(days = 2)).strftime("%Y-%m-%d 16:00:00"),
            "intervals": ["5minute", "15minute"],
        },
        "plot": False,
        "strategyName": "FiveEMA",
        "strategy": Strategy2,
        "optimization": True
    }
}


def getConfig(backtest_start_date):
    new_config = config

    now = datetime.strptime(str(backtest_start_date), "%Y-%m-%d %H:%M:%S")

    new_config["shortlisting"]["interval"]["start_datetime"] = (now - timedelta(days = 60)).strftime("%Y-%m-%d %H:%M:%S")
    new_config["shortlisting"]["interval"]["end_datetime"] = (now - timedelta(days = 2)).strftime("%Y-%m-%d 09:15:00")

    new_config["backtesting"]["interval"]["start_datetime"] = (now - timedelta(days = 1)).strftime("%Y-%m-%d 09:15:00")
    new_config["backtesting"]["interval"]["end_datetime"] = (now - timedelta(days = 0)).strftime("%Y-%m-%d 09:30:00")

    return new_config