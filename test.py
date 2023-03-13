from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import argparse

import backtrader as bt
import backtrader.feeds as btfeeds
import backtrader.indicators as btind


class SMAStrategy(bt.Strategy):
    params = (
        ('period', 10),
        ('onlydaily', False),
    )

    def __init__(self):
        self.sma_small_tf = btind.SMA(self.data, period=self.p.period)
        if not self.p.onlydaily:
            self.sma_large_tf = btind.SMA(self.data1, period=self.p.period)

    def nextstart(self):

        super(SMAStrategy, self).nextstart()


def runstrat():

    date2num('2023-02-03 11:11:13')

    args = parse_args()

    # Create a cerebro entity
    cerebro = bt.Cerebro(stdstats=False)

    # Add a strategy
    if not args.indicators:
        cerebro.addstrategy(bt.Strategy)
    else:
        cerebro.addstrategy(
            SMAStrategy,

            # args for the strategy
            period=args.period,
            onlydaily=args.onlydaily,
        )

    # Load the Data
    datapath = args.dataname or './data/temp/ADANIGREEN-5minute.txt'
    data = btfeeds.BacktraderCSVData(dataname=datapath)
    cerebro.adddata(data)  # First add the original data - smaller timeframe

    # tframes = dict(daily=bt.TimeFrame.Days, weekly=bt.TimeFrame.Weeks,
    #                monthly=bt.TimeFrame.Months)
    tframes = dict(ticker=bt.TimeFrame.Ticks ,minutes=bt.TimeFrame.Minutes ,daily=bt.TimeFrame.Days, weekly=bt.TimeFrame.Weeks,
                   monthly=bt.TimeFrame.Months)

    # Handy dictionary for the argument timeframe conversion
    # Resample the data
    if args.noresample:
        datapath = args.dataname2 or '../../datas/2006-week-001.txt'
        data2 = btfeeds.BacktraderCSVData(dataname=datapath)
        # And then the large timeframe
        cerebro.adddata(data2)
    else:
        cerebro.resampledata(data, timeframe=tframes[args.timeframe],
                             compression=args.compression)

    # Run over everything
    cerebro.run()

    # Plot the result
    cerebro.plot(style='bar')


def parse_args():
    parser = argparse.ArgumentParser(
        description='Multitimeframe test')

    parser.add_argument('--dataname', default='', required=False,
                        help='File Data to Load')

    parser.add_argument('--dataname2', default='', required=False,
                        help='Larger timeframe file to load')

    parser.add_argument('--noresample', action='store_true',
                        help='Do not resample, rather load larger timeframe')

    parser.add_argument('--timeframe', default='ticker', required=False,
                        choices=['ticker','minutes','daily', 'weekly', 'monhtly'],
                        help='Timeframe to resample to')

    parser.add_argument('--compression', default=50, required=False, type=int,
                        help='Compress n bars into 1')

    parser.add_argument('--indicators', action='store_true',
                        help='Wether to apply Strategy with indicators')

    parser.add_argument('--onlydaily', action='store_true',
                        help='Indicator only to be applied to daily timeframe')

    parser.add_argument('--period', default=10, required=False, type=int,
                        help='Period to apply to indicator')

    return parser.parse_args()


if __name__ == '__main__':
    runstrat()