"""
Trend strategy.

"""

from backtesting.strategy import BacktestingStrategy
from backtesting.technical import ma


class SMAStrategy(BacktestingStrategy):

    def __init__(self, feed, instrument):
        super(SMAStrategy, self).__init__(feed)

        # We want a 15 period SMA over the closing prices.
        self.__sma = ma.SMA(feed[instrument].getCloseDataSeries(), 15)
        self.__instrument = instrument

    def onBars(self, bars):
        bar = bars[self.__instrument]
        self.info("%s %s" % (bar.getClose(), self.__sma[-1]))
