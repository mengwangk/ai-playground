"""
=======================
Google Finance source
=======================
"""


# https://stackoverflow.com/questions/50394873/import-pandas-datareader-gives-importerror-cannot-import-name-is-list-like
import pandas as pd
pd.core.common.is_list_like = pd.api.types.is_list_like

import pandas_datareader.data as web


class GoogleFinanceSource():
    """ Google Finance source """

    _DATA_SOURCE = 'google'

    def __init__(self, ticker):
        """ Constructor """
        self.ticker = ticker

    def get_stock_historical_prices(self, start_date, end_date):
       """
       Get historical stock prices.

       :param start_date: Start date.
       :param end_date: End date.
       :return: Stock historical prices.
       """
       return web.DataReader(self.ticker, self._DATA_SOURCE, start_date, end_date)




