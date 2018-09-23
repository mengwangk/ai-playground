# -*- coding: utf-8 -*-
#
# Get stocks historical prices.

import os
import csv
import datetime as dt

import scrapy
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class OhlcSpiderInvesting(scrapy.Spider):
    """ Historical history scraper """
    name = "ohlc_investing"

    _URL_BASE = "{}-historical-data"
    _TICKER_FILE = "KLSE_selected.csv"
    _CHROME_DRIVER = '/Users/mengwangk/workspace/software/chromedriver/chromedriver'

    _END_DATE = dt.datetime.today().strftime('%m-%d-%Y')
    _START_DATE = dt.date(dt.date.today().year - 3, 1, 1).strftime('%m-%d-%Y')

    def start_requests(self):
        self.driver = webdriver.Chrome(self._CHROME_DRIVER)
        with open(self._TICKER_FILE, 'r') as f:
            reader = csv.reader(f)
            next(reader, None)  # skip the headers
            stock_list = list(reader)

        urls = []
        for stock in stock_list:
            urls.append(self._URL_BASE.format(stock[4]))

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        """Extract historical prices"""
        self.driver.get(response.url)
        code = response.xpath('//*[@id="quotes_summary_current_data"]/div[2]/div[4]/span[2]/text()').extract()
        try:
            # price_date_range = "{} - {}".format(self._START_DATE, self._END_DATE)
            # script_date_range = 'arguments[0].innerText = "{}";'.format(price_date_range)
            date_picker = self.driver.find_elements_by_xpath('//*[@id="datePickerIconWrap"]')
            date_picker[1].click()  # Look like there are 2 date pickers
            # ActionChains(self.driver).click(date_picker)

            # date_range = self.driver.find_element_by_xpath('//*[@id="widgetFieldDateRange"]')
            # self.driver.execute_script(script_date_range, date_range)

            # Start date
            # set_start_date  = 'arguments[0].innerText = "{}";'.format(self._START_DATE)
            start_date = self.driver.find_element_by_xpath('//*[@id="startDate"]')
            start_date.clear()
            start_date.send_keys(self._START_DATE)
            # self.driver.execute_script(set_start_date, start_date)

            # End date
            # set_end_date = 'arguments[0].innerText = "{}";'.format(self._END_DATE)
            end_date = self.driver.find_element_by_xpath('//*[@id="endDate"]')
            end_date.clear()
            end_date.send_keys(self._END_DATE)
            # self.driver.execute_script(set_end_date, end_date)

            WebDriverWait(self.driver, 300).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="applyBtn"]'))
            )

            apply_date_range = self.driver.find_element_by_xpath('//*[@id="applyBtn"]')
            # ActionChains(self.driver).click(apply_date_range)
            apply_date_range.click()

            element = WebDriverWait(self.driver, 300).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="curr_table"]'))
            )

            # Scrap the historical prices
            prices_rows = self.driver.find_elements_by_xpath('//*[@id="curr_table"]/tbody/tr')

            # print("{}: {}".format("Date", cols[0].get_attribute("innerText")))
            file_name = "{}.csv".format(code[0])
            file_exists = os.path.isfile(file_name)
            with open(file_name, 'w+', encoding='utf-8') as f:
                writer = csv.writer(f)
                if not file_exists:
                    writer.writerow(['date', 'price', 'open', 'high', 'low', 'volume', 'change_percent'])
                for row in prices_rows:
                    cols = row.find_elements_by_xpath(".//td")
                    writer.writerow([
                        cols[0].get_attribute("innerText"),
                        cols[1].get_attribute("innerText"),
                        cols[2].get_attribute("innerText"),
                        cols[3].get_attribute("innerText"),
                        cols[4].get_attribute("innerText"),
                        cols[5].get_attribute("innerText"),
                        cols[6].get_attribute("innerText")
                        ])
        except Exception as e:
            print(e)
        finally:
            print('Completed for {}'.format(code))
            # self.driver.close()
