
import pandas as pd

from source import YahooFinanceSource


class DividendYield():
    """
    Fundamental analysis using dividend yield.
    """

    def __init__(self, ticker):
        self.ticker = ticker

    # Public method to get stock historical dividends
    def get_stock_dividend_history(self, start_date, end_date, time_interval):
        yahooFinanceSource = YahooFinanceSource(self.ticker)
        return yahooFinanceSource.get_historical_stock_dividend_data(start_date, end_date, time_interval)


    def generate_stock_dividend_history_file(self, file_path, start_date, end_date, time_interval):
        dividend_data = self.get_stock_dividend_history(start_date, end_date, time_interval)
        print(dividend_data)
        return


