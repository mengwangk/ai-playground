"""
=================================
myInvestor-toolkit startup script
=================================
"""

import datetime as dt

from fundamental import DividendYield


class StockAnalysis:
    """
    Stock analysis.
    """

    _YEARS_INTERVAL = 5

    def __init__(self,
                 ticker,
                 start_date=dt.date(dt.date.today().year - _YEARS_INTERVAL, 1, 1).strftime('%Y-%m-%d'),
                 end_date=dt.datetime.today().strftime('%Y-%m-%d')):
        """
        Constructor.

        :param ticker: Stock ticker.L
        :param start_date: Analysis start date.
        :param end_date: Analysis end date.
        """
        self.ticker = ticker

    def fund_get_dividend_yields(self):
        dividend_yield = DividendYield(self.ticker)


def main():
    """
    Main script.
    """

    stock_analysis = StockAnalysis("6742.KL")


if __name__ == "__main__":
    main()
