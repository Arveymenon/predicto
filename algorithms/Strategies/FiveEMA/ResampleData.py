import backtrader as bt
import pandas as pd

class ResampledData(bt.feeds.PandasData):
    params = (
        ('timeframe', bt.TimeFrame.Weeks),
        ('compression', 1),
        ('method', 'last'),
    )

    def __init__(self, data, **kwargs):
        self._timeframe = self.p.timeframe
        self._compression = self.p.compression
        self._method = self.p.method
        self._resampled_data = self._resample_data(data)
        super().__init__(self._resampled_data)

    def start(self):
        super().start()
        self._resampled_data.start()

    def stop(self):
        super().stop()
        self._resampled_data.stop()

    def _resample_data(self, data):
        # Convert the data to a Pandas DataFrame
        df = data.to_dataframe()

        # Resample the data using the PandasResampler class
        ohlc_dict = {
            'Open': 'first',
            'High': 'max',
            'Low': 'min',
            'Close': 'last',
            'Volume': 'sum',
        }
        resampled_df = df.resample('W-MON', closed='left', label='left').apply(ohlc_dict)

        # Convert the resampled data back to a Backtrader-compatible format
        resampled_data = bt.feeds.PandasData(dataname=resampled_df)

        return resampled_data