import datetime as dt
import os
import pandas as pd

from source import YahooFinanceSource


class DividendYield():
    """
    Fundamental analysis using dividend yield.
    """

    # Default to current year
    _END_DATE = dt.datetime.today().strftime('%Y-%m-%d')

    # Default to last 5 years
    _YEAR_INTERVAL = 5

    # Default dataset directory
    _DATA_DIR = 'dataset'

    # Default generated file name
    _FILE_NAME = 'dividend_yield'

    def __init__(self, ticker, year_interval = _YEAR_INTERVAL):
        """
        Constructor
        :param ticker: Symbol or list of symbols.
        """
        self.ticker = ticker
        self._START_DATE = dt.date(dt.date.today().year - year_interval, 1, 1).strftime('%Y-%m-%d')


    def _file_path(self, file_name, base_dir):
        """
        Return the absolute path to the generated dividend csv file.

        :param file_name: File name without any extension.
        :param base_dir: Base directory.
        :return: Absolute path to the CSV file.
        """
        return os.path.abspath(os.path.join(base_dir, '{}.csv'.format(file_name)))

    def get_history(self, start_date=_START_DATE, end_date=_END_DATE, time_interval='daily'):
        """
        Public method to get stock historical dividends.

        :param start_date: History start date.
        :param end_date: History end date.
        :param time_interval: Interval.
        :return: Historical dividend data
        """
        yahooFinanceSource = YahooFinanceSource(self.ticker)
        return yahooFinanceSource.get_historical_stock_dividend_data(start_date, end_date, time_interval)

    def generate_history_file(self, file_name=_FILE_NAME, base_dir=_DATA_DIR, start_date=_START_DATE,
                              end_date=_END_DATE, time_interval='daily'):
        """
        Generate dividend yield CSV file.

        :param file_name: File name.
        :param base_dir: Base directory.
        :param start_date: History start date.
        :param end_date: History end date.
        :param time_interval: Interval.
        :return: Absolute path to the generated file.
        """
        abs_file_name = self._file_path(file_name, base_dir)
        if (os.path.exists(abs_file_name)):
            dividend_data = pd.read_csv(abs_file_name)
            dividend_data = dividend_data.set_index(['symbol', 'date'])
        else:
            dividend_data = pd.DataFrame()

        stock_dividends = self.get_history(start_date, end_date, time_interval)

        for symbol, values in stock_dividends.items():
            prices = values['prices']
            dividend_list = []
            for dividend in prices:
                dividend_list.append(pd.Series(dividend))
            df = pd.DataFrame(dividend_list)
            df['symbol'] = symbol
            df = df.set_index(['symbol', 'date'])
            if (dividend_data.empty):
                dividend_data = df
            else:
                dividend_data = dividend_data.combine_first(df)

        dividend_data.to_csv(abs_file_name, encoding='utf-8')
        return abs_file_name
