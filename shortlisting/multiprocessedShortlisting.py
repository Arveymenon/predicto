import multiprocessing
from shortlisting.shortlisting import shortlist

def multiProcessedShortlisting(
            symbols, 
            backtestTimeFrame, datetime_format, interval, 
            strategy,
            shortlisted_stocks,
            plot
        ):
         # ---------------------- Back testing ---------------------------#

            pool = multiprocessing.Pool()
            args = [(symbol, 
                     backtestTimeFrame[0], backtestTimeFrame[1], datetime_format, interval, 
                     strategy,
                     shortlisted_stocks,
                     plot
                     ) for symbol in symbols]
            pool.starmap(shortlist, args)
            pool.close()
            pool.join()