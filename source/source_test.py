"""
Tests for the source module.
"""

import unittest
import datetime as dt
import time as tm

from yahoofinance import YahooFinanceSource

class SourceTest(unittest.TestCase):

    def test_get_stocks(self):
        print("Getting the stocks")
        tech_stocks = ['6742.KL']

        today = dt.datetime.today().strftime('%Y-%m-%d')

        yahoo_finance_source = YahooFinanceSource(tech_stocks)
        historical_data = yahoo_finance_source.get_historical_stock_data('2017-05-15', today, 'daily')
        print(historical_data)





