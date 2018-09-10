# -*- coding: utf-8 -*-
#
# Get the stock quotes
#
# https://sqa.stackexchange.com/questions/26741/how-to-make-a-selection-from-a-dropdown-using-selenium-python
# https://stackoverflow.com/questions/39928515/python-error-with-web-driver-selenium
# https://sqa.stackexchange.com/questions/28823/wait-until-in-select-element-using-selenium/28837
# https://selenium-python.readthedocs.io/waits.html

import csv
import os

import scrapy
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait


class QuotesSpiderInvesting(scrapy.Spider):
    """
    Scrap Malaysia equities from investing.com
    """

    name = "quotes_investing"

    _URL_BASE = 'https://www.investing.com/equities/malaysia'
    _CHROME_DRIVER = '/Users/mengwangk/workspace/software/chromedriver/chromedriver'
    _TICKER_FILE = "KLSE_investing.csv"

    def start_requests(self):
        urls = [self._URL_BASE]
        self.driver = webdriver.Chrome(self._CHROME_DRIVER)

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        """Extract the symbol and the name into a list"""
        self.driver.get(response.url)

        try:
            select_stocks = Select(self.driver.find_element_by_xpath('//*[@id="stocksFilter"]'))
            # print([o.text for o in select_stocks.options])
            select_stocks.select_by_index(0)  # Malaysia all stocks

            element = WebDriverWait(self.driver, 300).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="cross_rate_markets_stocks_1"]'))
            )

            # Scrap the stocks
            stocks_rows = self.driver.find_elements_by_xpath('//*[@id="cross_rate_markets_stocks_1"]/tbody/tr')
            for row in stocks_rows:
                cols = row.find_elements_by_xpath(".//td")
                # print("{}: {}".format("Link", cols[1].find_element_by_xpath(".//a").get_attribute("href")))
                # print("{}: {}".format("Name", cols[1].find_element_by_xpath(".//a").get_attribute("innerText")))
                # print("{}: {}".format("Last", cols[2].get_attribute("innerText")))
                # print("{}: {}".format("High", cols[3].get_attribute("innerText")))
                # print("{}: {}".format("Low", cols[4].get_attribute("innerText")))
                # print("{}: {}".format("Change", cols[5].get_attribute("innerText")))
                # print("{}: {}".format("Change %", cols[6].get_attribute("innerText")))
                # print("{}: {}".format("Volume", cols[7].get_attribute("innerText")))
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
            self.driver.close()
