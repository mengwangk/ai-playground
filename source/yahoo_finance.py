"""
=======================
Yahoo Finance source
Version: 0.0.1
=======================
"""

import re
import requests
import time
from json import loads
from bs4 import BeautifulSoup
from yahoofinancials import YahooFinancials


# Yahoo Finance data source
class YahooFinanceSource(YahooFinancials):

    def __init__(self, ticker):
        super(YahooFinanceSource, self).__init__(ticker)

    # private static method to scrap data from yahoo finance
    @staticmethod
    def _scrape_dividend_data(url, tech_type, statement_type):
        response = requests.get(url)
        time.sleep(7)
        soup = BeautifulSoup(response.content, "html.parser")
        script = soup.find("script", text=re.compile("root.App.main")).text
        data = loads(re.search("root.App.main\s+=\s+(\{.*\})", script).group(1))
        stores = data["context"]["dispatcher"]["stores"]["HistoricalPriceStore"]
        return stores


    # Private Method to clean the dates of the newly returns historical stock data into readable format
    def _clean_historical_div_data(self, hist_data):
        data = {}
        for k, v in hist_data.items():
            if 'date' in k.lower():
                cleaned_date = self.format_date(v, 'standard')
                dict_ent = {k: {u'' + 'formatted_date': cleaned_date, 'date': v}}
                data.update(dict_ent)
            elif isinstance(v, list):
                sub_dict_list = []
                for sub_dict in v:
                    type = sub_dict.get('type', '')
                    if (type.upper() == 'DIVIDEND'):
                        sub_dict[u'' + 'formatted_date'] = self.format_date(sub_dict['date'], 'standard')
                        sub_dict_list.append(sub_dict)
                dict_ent = {k: sub_dict_list}
                data.update(dict_ent)
            else:
                dict_ent = {k: v}
                data.update(dict_ent)
        return data


    # Private method to get time interval code
    def _build_historical_dividend_url(self, ticker, hist_oj, filter='div'):
        url = self._BASE_YAHOO_URL + ticker + '/history?period1=' + str(hist_oj['start']) + '&period2=' + \
              str(hist_oj['end']) + '&interval=' + hist_oj['interval'] + '&filter=' + filter + '&frequency=' + \
              hist_oj['interval']
        return url


    # Private Method to take scrapped data and build a data dictionary with
    def _create_dict_ent_div(self, ticker, statement_type, tech_type, report_name, hist_obj):
        up_ticker = ticker.upper()
        YAHOO_URL = self._build_historical_dividend_url(up_ticker, hist_obj)
        re_data = self._scrape_dividend_data(YAHOO_URL, tech_type, statement_type)
        cleaned_re_data = self._clean_historical_div_data(re_data)
        dict_ent = {up_ticker: cleaned_re_data}
        return dict_ent


    # Public Method for user to get historical stock dividend data
    def get_historical_stock_dividend_data(self, start_date, end_date, time_interval):
        interval_code = self.get_time_code(time_interval)
        start = self.format_date(start_date, 'unixstamp')
        end = self.format_date(end_date, 'unixstamp')
        hist_obj = {'start': start, 'end': end, 'interval': interval_code}
        data = self.get_stock_dividend_data('history', hist_obj=hist_obj)
        return data


    # Public Method to get stock data
    def get_stock_dividend_data(self, statement_type='history', tech_type='', report_name='', hist_obj={}):
        data = {}
        if isinstance(self.ticker, str):
            dict_ent = self._create_dict_ent_div(self.ticker, statement_type, tech_type, report_name, hist_obj)
            data.update(dict_ent)
        else:
            for tick in self.ticker:
                dict_ent = self._create_dict_ent_div(tick, statement_type, tech_type, report_name, hist_obj)
                data.update(dict_ent)
        return data
