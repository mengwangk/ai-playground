"""
Test strategy.

"""

from backtesting.strategy import BacktestingStrategy


class TestStrategy(BacktestingStrategy):

    def __init__(self, feed, instrument):
        super(TestStrategy, self).__init__(feed)
        self.__instrument = instrument

    def onBars(self, bars):
        bar = bars[self.__instrument]
        self.info(bar.getClose())
