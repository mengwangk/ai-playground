"""
=================================
myInvestor-toolkit startup script
=================================
"""

import os

import pandas as pd

from source import YahooFinanceSource
from fundamental import DividendYield


class StockAnalysis:
    """
    Stock analysis.
    """

    _TICKER_FILE = 'dataset/ticker.csv'

    _CURRENT_PRICE_FILE = 'dataset/current_price.csv'

    def fund_update_dividend_yields_for_exchange(self, exchange):
        """
        Update existing dividend yield file.

        :param exchange: Exchange symbol.
        :return: None
        """

        print('Updating dividend yields for {}'.format(exchange))
        df_dividend_data = pd.read_csv('dataset/{}_dividend_yields.csv'.format(exchange), dtype=str)
        # Check if dividend file exists

    def fund_get_dividend_yields_for_exchange(self, exchange, skip_if_exist=True):
        """
        Get dividends yields for the exchange.

        :param exchange: Exchange symbol.
        :param skip_if_exist: Skip if the dividend yields already in the file.
        :return: True on success, otherwise return False.
        """
        df_stocks = pd.read_csv(self._TICKER_FILE, dtype=str)
        df_stocks = df_stocks.loc[df_stocks['Exchange'] == exchange]
        df_stocks = df_stocks.set_index(['Ticker'])

        count = len(df_stocks)
        index = 1

        if (count == 0): return

        dividend_file = 'dataset/{}_dividend_yields.csv'.format(exchange)
        if (os.path.exists(dividend_file)):
            df_dividend_data = pd.read_csv(dividend_file)
            df_dividend_data = df_dividend_data.set_index(['symbol', 'date'])
        else:
            df_dividend_data = pd.DataFrame()

        for ticker, row in df_stocks.iterrows():
            print('{} / {} - Getting dividend yields for {}'.format(index, count, ticker))
            index = index + 1

            # Skip if already exist
            if (skip_if_exist):
                if not df_dividend_data.empty and ticker in df_dividend_data.index:
                    print('Skipping {}'.format(ticker))
                    continue

            try:
                dividend_yield = DividendYield(ticker)
                stock_dividends = dividend_yield.get_history()

                for symbol, values in stock_dividends.items():
                    prices = values['prices']
                    dividend_list = []
                    for dividend in prices:
                        dividend_list.append(pd.Series(dividend))
                    if len(dividend_list) > 0:
                        df_dividend = pd.DataFrame(dividend_list)
                        df_dividend['symbol'] = symbol
                        df_dividend = df_dividend.set_index(['symbol', 'date'])
                        if (df_dividend_data.empty):
                            df_dividend_data = df_dividend
                        else:
                            df_dividend_data = df_dividend_data.combine_first(df_dividend)
                        df_dividend_data.to_csv(dividend_file, encoding='utf-8')
            except Exception as e:
                print('Ooops...error with {} - {}'.format(ticker, str(e)))
                continue

            return True

        return False

    def fund_get_stock_financials(self, ticker_file, price_file_name=_CURRENT_PRICE_FILE):
        """
        Getting current prices into a file.

        :param ticker_file: Ticket file.
        :param price_file_name: Output price file name.
        :return: True on success, otherwise return False.
        """

        df_stocks = pd.read_csv(ticker_file, dtype=str)
        tickers = df_stocks.symbol.unique()
        current = 1
        df_all_stocks_summaries = pd.DataFrame()
        for ticker in tickers:
            print('{} - Getting current info for {}.'.format(current, ticker))
            current = current + 1

            yahoo_finance_source = YahooFinanceSource(ticker)
            stock_summary_data = yahoo_finance_source.get_stock_summary_data()
            stock_summary_data[ticker]['symbol'] = ticker
            df_stock_summary = pd.DataFrame([pd.Series(stock_summary_data[ticker])])
            if (df_all_stocks_summaries.empty):
                df_all_stocks_summaries = df_stock_summary
            else:
                df_all_stocks_summaries = df_all_stocks_summaries.append(df_stock_summary)

            df_all_stocks_summaries.to_csv(price_file_name, encoding='utf-8', index=False)


def main():
    """
    Main script.
    """

    stock_analysis = StockAnalysis()

    # stock_analysis.fund_get_dividend_yields_for_exchange('KLS')

    stock_analysis.fund_get_stock_financials(ticker_file='dataset/KLS_selected_equities.csv',
                                            price_file_name='dataset/KLS_stock_financials.csv')

    # yahoo_finance_source = YahooFinanceSource("6742.KL")
    # stock_summary_data = yahoo_finance_source.get_stock_summary_data()
    # print(stock_summary_data)


if __name__ == "__main__":
    main()
