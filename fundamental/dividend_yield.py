import datetime as dt
import os

from source import YahooFinanceSource


class DividendYield():
    """
    Fundamental analysis using dividend yield.
    """

    # Default to current year
    _END_DATE = dt.datetime.today().strftime('%Y-%m-%d')

    # Default to last 5 year
    _START_DATE = dt.date(dt.date.today().year - 5, 1, 1).strftime('%Y-%m-%d')

    _DATA_DIR = 'dataset'

    def __init__(self, ticker):
        """
        Constructor
        :param ticker: Symbol or list of symbols.
        """
        self.ticker = ticker

    def _file_path(self, file_name, base_dir=_DATA_DIR):
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

        :param start_date:
        :param end_date:
        :param time_interval:
        :return: Historical dividend data
        """
        yahooFinanceSource = YahooFinanceSource(self.ticker)
        return yahooFinanceSource.get_historical_stock_dividend_data(start_date, end_date, time_interval)

    def generate_history_file(self, file_name, start_date=_START_DATE, end_date=_END_DATE, time_interval='daily'):
        """

        :param file_name:
        :param start_date:
        :param end_date:
        :param time_interval:
        :return:
        """
        abs_file_name = self._file_path(file_name)
        print(abs_file_name)
        # dividend_data = self.get_history(start_date, end_date, time_interval)
        # print(dividend_data)
        return
