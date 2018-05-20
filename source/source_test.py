"""
Tests for the source module.
"""

import unittest
import datetime as dt
import time as tm

import yahoofinance
import googlefinance

from yahoofinancials import YahooFinancials

class SourceTest(unittest.TestCase):

    def test_get_stocks(self):
        print("Getting the stocks")
        tech_stocks = ['YTLPOWR']

        today = dt.datetime.today().strftime('%Y-%m-%d')
        print(today)

        #yahoo_financials = YahooFinancials(tech_stocks)
        #historical_data = yahoo_financials.get_historical_stock_data('2008-09-15', '2018-09-1', 'daily')
        #print(historical_data)




