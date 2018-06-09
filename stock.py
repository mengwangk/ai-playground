"""
=================================
myInvestor-toolkit startup script
=================================
"""

import pandas as pd
import datetime as dt
import time as tm
from dateutil.relativedelta import relativedelta

from fundamental import DividendYield


class StockAnalysis:
    """
    Stock analysis.
    """


    def __init__(self, ticker, start_date=dt.datetime.today().strftime('%Y-%m-%d'),
                 end_date=(dt.datetime.now() - relativedelta(years=5)).strftime('%Y-%m-%d')):
        """
        Constructor.

        :param ticker: Stock ticker.
        :param start_date: Analysis start date.
        :param end_date: Analysis end date.
        """
        self.ticker = ticker
        print('{} {} {}'.format(ticker, start_date, end_date))


    def fund_get_dividend_yields(self):
        dividend_yield = DividendYield(self.ticker)


def main():
    """
    Main script.
    """

    stock_analysis = StockAnalysis("6742.KL")


if __name__ == "__main__":
    main()
