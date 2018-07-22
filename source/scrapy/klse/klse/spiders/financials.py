# -*- coding: utf-8 -*-
#
# Get stocks financial information

import csv
import os

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

    def _strip(self, val):
        return val.replace('\xa0', ' ')

    def parse(self, response):
        code = response.request.url.split('/')[-1].split('.')[0]
        market_cap = response.xpath(
            '//*[@id="content"]/table[2]/tr/td[1]/table[1]/tr/td[2]/table/tr[1]/td[2]/b/text()').extract()

        file_exists = os.path.isfile(self._FINANCIALS_FILE)
        with open(self._FINANCIALS_FILE, 'a', encoding='utf-8') as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(['market_cap'])
            writer.writerow(market_cap)
