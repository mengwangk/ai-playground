# -*- coding: utf-8 -*-
#
# Get stocks dividend histories

import csv

import scrapy


class DividendHistorySpider(scrapy.Spider):
    """ Dividend history scraper """
    name = "dividend_history"

    _URL_BASE = "https://klse.i3investor.com/servlets/stk/annent/{}.jsp"
    _TICKER_FILE = "KLSE.csv"

    def start_requests(self):
        with open(self._TICKER_FILE, 'r') as f:
            reader = csv.reader(f)
            stock_list = list(reader)

        urls = []
        for stock in stock_list:
            urls.append(self._URL_BASE.format(stock[2]))

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        print("parsing response")
