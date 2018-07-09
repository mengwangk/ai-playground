# -*- coding: utf-8 -*-

"""Test for various sources

Supported sources
- Yahoo Finance
- I3Investor - KLSe

"""


import unittest
import datetime as dt
import string

from source import YahooFinanceSource

class SourceTest(unittest.TestCase):

    _TEST_SYMBOL = '6742.KL'

    _YAHOO_FINANCE_SOURCE = YahooFinanceSource(_TEST_SYMBOL)
    _TODAY  = dt.datetime.today().strftime('%Y-%m-%d')

    @unittest.skip
    def test_yahoo_get_stock_prices(self):
        print("Getting historical prices")

        # Get historical stock data
        historical_data = self._YAHOO_FINANCE_SOURCE.get_historical_stock_data('2016-05-15', self._TODAY, 'daily')
        print(historical_data)

        # prices = historical_data[self._TEST_SYMBOL]['prices']
        # print(prices)
        # for price in prices:
        #     print(price.get('close', None))


        # Get current price
        # current_price = yahoo_finance_source.get_current_price()
        # print(current_price)

    @unittest.skip
    def test_yahoo_get_dividend_history(self):
        print("Getting historical dividends")
        dividend_data = self._YAHOO_FINANCE_SOURCE.get_historical_stock_dividend_data('2010-05-15', self._TODAY, 'daily')
        print(dividend_data)


    def test_genereate_a_toz(self):
        for c in string.ascii_uppercase:
            print(c)
