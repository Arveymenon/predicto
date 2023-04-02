import multiprocessing
from shortlisting.shortlisting import shortlist

def multiProcessedShortlisting(
            symbols, 
            backtestTimeFrame, datetime_format, interval, 
            strategy,
            shortlisted_stocks,
            plot = False
        ):
         # ---------------------- Shortlisting testing ---------------------------#

            pool = multiprocessing.Pool()
            start_date = backtestTimeFrame[0]
            end_date = backtestTimeFrame[1]
            
            args = [(symbol,
                     start_date, end_date, datetime_format, interval,
                     strategy,
                     shortlisted_stocks,
                     plot
                     ) for symbol in symbols]
            
            try:
                pool.starmap(shortlist, args)
            except Exception as e:
                print(f"Error: {e}")
            finally:
                pool.close()
                pool.join()