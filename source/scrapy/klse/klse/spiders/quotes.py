# -*- coding: utf-8 -*-
#
# Get the stock quotes

import os
import string

import pandas as pd
import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"

    _URL_BASE = 'https://klse.i3investor.com/jsp/stocks.jsp?g=S&m=int&s=%s'
    _TICKER_FILE = "KLSE.csv"

    def _chunks(self, l, n):
        """Yield successive n-sized chunks from l."""
        for i in range(0, len(l), n):
            yield l[i:i + n]

    def start_requests(self):
        urls = []
        urls.append(self._URL_BASE % '0')
        for c in string.ascii_uppercase:
            urls.append(self._URL_BASE % c)

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        """Extract the symbol and the name into a list"""

        if (os.path.exists(self._TICKER_FILE)):
            df_symbols = pd.read_csv(self._TICKER_FILE, dtype=str)
            df_symbols.set_index(['symbol'])
        else:
            df_symbols = pd.DataFrame()

        stock_listing = response.css('.left a::text').extract()
        df = pd.DataFrame(list(self._chunks(stock_listing, 2)), columns=["symbol", "name"])
        df.set_index(['symbol'])

        if (df_symbols.empty):
            df_symbols = df
        else:
            print(df)
            df_symbols = df_symbols.append(df)

        df_symbols.to_csv(self._TICKER_FILE, encoding='utf-8', index=False)

        # pprint.pprint(list(self._chunks(stock_listing, 2)))
