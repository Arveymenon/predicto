import pandas as pd
from datetime import datetime

def isHoliday(date: datetime):
    df = pd.read_csv(r'./data/NSEHolidays.csv')
    if(str(date.date()) in df["date"].values or isWeekend(date)):
        return True
    else:
        return False

def isWeekend(date: datetime):
    return (date.isoweekday() == 7 or date.isoweekday() == 6)

# TODO: Code to convert date to dataframe format
# df = pd.read_csv(r'./data/NSEHolidays.csv')
# df['date'] = df['date'].apply(lambda x:
#                     datetime.strptime(x, "%d-%m-%Y")
#                 )
# df.to_csv(r'./data/NSEHolidays.csv')