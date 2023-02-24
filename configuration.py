from datetime import datetime, timedelta
from algorithms.Strategies.Shortlisting.InsideDay.InsideDay import InsideDayStrategy
from algorithms.Strategies.FiveEMA.Strategy import Strategy

config = {
    "temp_files_path": "./data/temp/",
    "input_file": "AllNSEStocksOnZerodha",
    "shortlisting": {
        "isActive": True,
        "intervals": {
            "datetime_format": "%Y-%m-%d %H:%M:%S",
            "start_datetime": (datetime.now() - timedelta(days = 21)).strftime("%Y-%m-%d %H:%M:%S"),
            "end_datetime": (datetime.now() - timedelta(days = 14)).strftime("%Y-%m-%d %H:%M:%S"),
            "intervals": ["day"],
        },
        "plot": True,
        "strategyName": "insideDay",
        "strategy": InsideDayStrategy
    },
    "backtesting": {
        "isActive": True,
        "intervals": {
            "datetime_format": "%Y-%m-%d %H:%M:%S",
            "start_datetime": (datetime.now() - timedelta(days = 14)).strftime("%Y-%m-%d %H:%M:%S"),
            "end_datetime": (datetime.now() - timedelta(days = 7)).strftime("%Y-%m-%d %H:%M:%S"),
            "intervals": ["day"],
        },
        "plot": True,
        "strategyName": "FiveEMA",
        "strategy": Strategy,
        "optimization": False
    },
    "forwardtesting": {
        "isActive": True,
        "intervals": {
            "datetime_format": "%Y-%m-%d %H:%M:%S",
            "start_datetime": (datetime.now() - timedelta(days = 7)).strftime("%Y-%m-%d %H:%M:%S"),
            "end_datetime": (datetime.now() - timedelta(days = 0)).strftime("%Y-%m-%d %H:%M:%S"),
            "intervals": ["day"],
        },
        "plot": True,
        "strategyName": "insideDay",
        "strategy": Strategy
    }
}

def getInputfile():
    return config["input_file"]