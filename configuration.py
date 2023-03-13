from datetime import datetime, timedelta

from algorithms.Strategies.Shortlisting.InsideDay.InsideDay import InsideDayStrategy
# from algorithms.Strategies.Shortlisting.Volitility import VolatilityStrategy
from algorithms.Strategies.Shortlisting.MMI import MMI

from algorithms.Strategies.FiveEMA.Strategy import Strategy
from algorithms.Strategies.FiveEMA.Strategy2 import Strategy2

# from algorithms.Strategies.Shortlisting.BBRSI import BBRSIStrategy
config = {
    "initialInvestment": 30000,
    "temp_files_path": "./data/temp/",
    "input_file": "nsesmallcap100",
    "shortlisting": {
        "isActive": False,
        "interval": {
            "datetime_format": "%Y-%m-%d %H:%M:%S",
            "start_datetime": (datetime.now() - timedelta(days = 32)).strftime("%Y-%m-%d 09:00:00"),
            "end_datetime": (datetime.now() - timedelta(days = 5)).strftime("%Y-%m-%d 09:00:00"),
            "intervals": ["day"],
        },
        "plot": False,
        "strategyName": "insideDay",
        "strategy": InsideDayStrategy
    },
    "backtesting": {
        "isActive": False,
        "interval": {
            "datetime_format": "%Y-%m-%d %H:%M:%S",
            "start_datetime": (datetime.now() - timedelta(days = 5)).strftime("%Y-%m-%d 09:00:00"),
            "end_datetime": (datetime.now() - timedelta(days = 4)).strftime("%Y-%m-%d 16:00:00"),
            "intervals": ["5minute", "15minute"],
        },
        "plot": False,
        "strategyName": "FiveEMA",
        "strategy": Strategy2,
        "optimization": False
    }
}

def getInputfile():
    return config["input_file"]


def getConfig(backtest_start_date):
    new_config = config

    now = datetime.strptime(str(backtest_start_date), "%Y-%m-%d %H:%M:%S")

    new_config["shortlisting"]["interval"]["start_datetime"] = (now - timedelta(days = 60)).strftime("%Y-%m-%d %H:%M:%S")
    new_config["shortlisting"]["interval"]["end_datetime"] = (now - timedelta(days = 2)).strftime("%Y-%m-%d 09:15:00")

    new_config["backtesting"]["interval"]["start_datetime"] = (now - timedelta(days = 1)).strftime("%Y-%m-%d 09:15:00")
    new_config["backtesting"]["interval"]["end_datetime"] = (now - timedelta(days = 0)).strftime("%Y-%m-%d 09:30:00")

    return new_config

# "forwardtesting": {
#     "isActive": True,
#     "interval": {
#         "datetime_format": "%Y-%m-%d %H:%M:%S",
#         "start_datetime": (datetime.now() - timedelta(days = 4)).strftime("%Y-%m-%d %H:%M:%S"),
#         "end_datetime": (datetime.now() - timedelta(days = 0)).strftime("%Y-%m-%d %H:%M:%S"),
#         "intervals": ["day"],
#     },
#     "plot": True,
#     "strategyName": "insideDay",
#     "strategy": Strategy
# }


# "start_datetime": (datetime.now() - timedelta(days = 40)).strftime("%Y-%m-%d 09:15:00"),
# "end_datetime": (datetime.now() - timedelta(days = 10)).strftime("%Y-%m-%d 03:30:00"),

# "start_datetime": (datetime.now() - timedelta(days = 9)).strftime("%Y-%m-%d 09:15:00"),
# "end_datetime": (datetime.now() - timedelta(days = 8)).strftime("%Y-%m-%d 03:30:00"),