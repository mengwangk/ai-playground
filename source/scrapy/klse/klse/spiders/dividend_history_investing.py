# -*- coding: utf-8 -*-
#
# Get stocks dividend histories

import csv
import os

import scrapy
from scrapy.selector import Selector


class DividendHistorySpiderI3Investor(scrapy.Spider):
    """ Dividend history scraper """
    name = "dividend_history_investing"

    _URL_BASE = "{}-dividends"
    _DIVIDENDS_FILE = "KLSE_dividends_investing.csv"
    _TICKER_FILE = "KLSE_investing.csv"
    _LOOKUP_FILE = "KLSE_lookup_investing.csv"

    def start_requests(self):
        with open(self._TICKER_FILE, 'r') as f:
            reader = csv.reader(f)
            next(reader, None)  # skip the headers
            stock_list = list(reader)

        urls = []
        for stock in stock_list:
            urls.append(self._URL_BASE.format(stock[1]))

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        code = list(map(str.strip, response.xpath('//*[@id="quotes_summary_current_data"]/div[2]/div[4]/span[2]/text()').extract()))
        name = list(map(str.strip, response.xpath('//*[@id="leftColumn"]/div[1]/h1/text()').extract()))
        selector = Selector(response)
        results = selector.xpath("//*[contains(@id, 'dividendsHistoryData')]")
        for result in results:
            ex_dividend_dates = result.xpath('.//tbody/tr/td[1]/text()').extract()
            dividends = result.xpath('.//tbody/tr/td[2]/text()').extract()
            payment_dates = result.xpath('.//tbody/tr/td[4]/text()').extract()
            yields = result.xpath('.//tbody/tr/td[5]/text()').extract()
            dividends = [code + name +  list(d) for d in zip(ex_dividend_dates, dividends, payment_dates, yields)]
            file_exists = os.path.isfile(self._DIVIDENDS_FILE)
            with open(self._DIVIDENDS_FILE, 'a') as f:
                writer = csv.writer(f)
                if not file_exists:
                    writer.writerow(['code', 'name', 'ex_dividend_date', 'dividend', 'payment_date', 'yield'])
                writer.writerows(dividends)

            ## Additionally, write the code and the URL to a file
            file_exists = os.path.isfile(self._LOOKUP_FILE)
            with open(self._LOOKUP_FILE, 'a') as f:
                writer = csv.writer(f)
                if not file_exists:
                    writer.writerow(['code', 'name', 'url'])
                writer.writerow([code[0], name[0], response.request.url])

