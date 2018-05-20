"""
=======================
Yahoo Finance source
Version: 0.0.1
=======================
"""

from yahoofinancials import YahooFinancials

# Yahoo Finance data source
class YahooFinanceSource(YahooFinancials):

    def __init__(self, ticker):
        super(YahooFinanceSource, self).__init__(ticker)

    # Public method to get historical dividends
    def get_historical_dividends(self):
        print("Get dividends history")