# -*- coding: utf-8 -*-
#
# Get stocks financial information

import csv

import scrapy


class FinancialsSpider(scrapy.Spider):
    """Stock financials scraper"""

    name = "financials"

    _URL_BASE = "https://klse.i3investor.com/servlets/stk/{}.jsp"
    _FINANCIALS_FILE = "KLSE_financials.csv"
    _TICKER_FILE = "KLSE.csv"

    def start_requests(self):
        with open(self._TICKER_FILE, 'r') as f:
            reader = csv.reader(f)
            next(reader, None)  # skip the headers
            stock_list = list(reader)

        urls = []
        for stock in stock_list:
            urls.append(self._URL_BASE.format(stock[2]))

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        print("Parsing the response")