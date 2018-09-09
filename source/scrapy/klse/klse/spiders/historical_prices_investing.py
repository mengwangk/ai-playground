# -*- coding: utf-8 -*-
#
# Get stocks historical prices

import csv
import os

import scrapy
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait


class HistoricalPricesSpiderInvesting(scrapy.Spider):
    """ Historical history scraper """
    name = "historical_prices_investing"

    _URL_BASE = "{}-historical-data"
    _TICKER_FILE = "KLSE_investing.csv"
    _CHROME_DRIVER = '/Users/mengwangk/workspace/software/chromedriver/chromedriver'

    def start_requests(self):
        self.driver = webdriver.Chrome(self._CHROME_DRIVER)
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
        """Extract historical prices"""
        self.driver.get(response.url)
        code = response.xpath('//*[@id="quotes_summary_current_data"]/div[2]/div[4]/span[2]/text()').extract()

        try:
            select_stocks = Select(self.driver.find_element_by_xpath('//*[@id="stocksFilter"]'))
            select_stocks.select_by_index(0)  # Malaysia all stocks

            element = WebDriverWait(self.driver, 300).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="cross_rate_markets_stocks_1"]'))
            )

            # Scrap the stocks
            stocks_rows = self.driver.find_elements_by_xpath('//*[@id="cross_rate_markets_stocks_1"]/tbody/tr')
            for row in stocks_rows:
                cols = row.find_elements_by_xpath(".//td")
                # print("{}: {}".format("Link", cols[1].find_element_by_xpath(".//a").get_attribute("href")))
                file_exists = os.path.isfile(self._TICKER_FILE)
                with open(self._TICKER_FILE, 'a', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    if not file_exists:
                        writer.writerow(['name', 'link', 'last', 'high', 'low', 'change', 'change_percent', 'volume'])
                    writer.writerow([
                        cols[1].find_element_by_xpath(".//a").get_attribute("innerText"),
                        cols[1].find_element_by_xpath(".//a").get_attribute("href"),
                        cols[2].get_attribute("innerText"),
                        cols[3].get_attribute("innerText"),
                        cols[4].get_attribute("innerText"),
                        cols[5].get_attribute("innerText"),
                        cols[6].get_attribute("innerText"),
                        cols[7].get_attribute("innerText")
                    ])
        except Exception as e:
            print(e)
        finally:
            self.driver.quit()
