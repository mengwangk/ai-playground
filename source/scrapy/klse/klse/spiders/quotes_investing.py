# -*- coding: utf-8 -*-
#
# Get the stock quotes
#
# https://sqa.stackexchange.com/questions/26741/how-to-make-a-selection-from-a-dropdown-using-selenium-python
# https://stackoverflow.com/questions/39928515/python-error-with-web-driver-selenium
# https://sqa.stackexchange.com/questions/28823/wait-until-in-select-element-using-selenium/28837
# https://selenium-python.readthedocs.io/waits.html

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

            element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "marketInnerContent"))
            )
        except Exception as e:
            print(e)
        finally:
            self.driver.close()
