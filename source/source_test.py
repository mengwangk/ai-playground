"""
Tests for the source module.
"""

import unittest
import datetime as dt
import time as tm

from source import YahooFinanceSource

class SourceTest(unittest.TestCase):

    def test_get_stocks(self):
        print("Getting the stocks")
        symbol = '6742.KL'

        today = dt.datetime.today().strftime('%Y-%m-%d')

        yahoo_finance_source = YahooFinanceSource(symbol)

        # Get historical dividends


        # Get current price
        # current_price = yahoo_finance_source.get_current_price()
        # print(current_price)

        # Get historical prices
        # historical_data = yahoo_finance_source.get_historical_stock_data('2017-05-15', today, 'daily')
        # prices = historical_data[symbol]['prices']
        # print(prices)
        # for price in prices:
        #     print(price.get('close', None))





