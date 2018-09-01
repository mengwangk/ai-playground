# -*- coding: utf-8 -*-
#
# Get stocks dividend histories

import csv
import os

import scrapy


class HistoricalPricesScraper(scrapy.Spider):
    """ Historical prices scraper """
    name = "historical_prices"

    _URL_BASE = "https://klse.i3investor.com/servlets/stk/rec/{}.jsp"
    _HISTORICAL_PRICES_FILE = "KLSE_historical_prices.csv"
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
        code = response.request.url.split('/')[-1].split('.')[0]
        ann_dates = response.xpath('//*[@id="entitlementTable"]/tbody/tr/td[1]/text()').extract()
        ex_dates = response.xpath('//*[@id="entitlementTable"]/tbody/tr/td[2]/text()').extract()
        payment_dates = response.xpath('//*[@id="entitlementTable"]/tbody/tr/td[3]/text()').extract()
        dividend_type = response.xpath('//*[@id="entitlementTable"]/tbody/tr/td[4]/text()').extract()
        subject = response.xpath('//*[@id="entitlementTable"]/tbody/tr/td[5]/text()').extract()
        amount = response.xpath('//*[@id="entitlementTable"]/tbody/tr/td[6]/text()').extract()

        dividends = [[code] + list(d) for d in zip(ann_dates, ex_dates, payment_dates, dividend_type, subject, amount)]
        file_exists = os.path.isfile(self._HISTORICAL_PRICES_FILE)

        with open(self._HISTORICAL_PRICES_FILE, 'a') as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(['code', 'ann_date', 'ex_date', 'payment_date', 'dividend_type', 'subject', 'amount'])
            writer.writerows(dividends)
