"""
Mixed strategy.

"""

from pyalgotrade.strategy import BacktestingStrategy
from pyalgotrade.technical import ma, rsi


class RsiSma(BacktestingStrategy):

    def __init__(self, feed, instrument):
        super(RsiSma, self).__init__(feed)

        self.__rsi = rsi.RSI(feed[instrument].getCloseDataSeries(), 14)
        self.__sma = ma.SMA(self.__rsi, 15)
        self.__instrument = instrument

    def onBars(self, bars):
        bar = bars[self.__instrument]
        self.info("%s %s %s" % (bar.getClose(), self.__rsi[-1], self.__sma[-1]))
