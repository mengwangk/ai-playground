"""
=================================
myInvestor-toolkit startup script
=================================
"""

import pandas as pd
import os

from fundamental import DividendYield


class StockAnalysis:
    """
    Stock analysis.
    """

    _TICKER_FILE = 'dataset/ticker.csv'

    def fund_get_dividend_yields_for_exchange(self, exchange, skip_if_exist=True):
        df_stocks = pd.read_csv(self._TICKER_FILE, dtype=str)
        df_stocks = df_stocks.loc[df_stocks['Exchange'] == exchange]
        df_stocks = df_stocks.set_index(['Ticker'])

        count = len(df_stocks)
        index = 1

        if (count == 0): return

        dividend_file = 'dataset/{}_dividend_yields.csv'.format(exchange)
        if (os.path.exists(dividend_file)):
            dividend_data = pd.read_csv(dividend_file)
            dividend_data = dividend_data.set_index(['symbol', 'date'])
        else:
            dividend_data = pd.DataFrame()

        for ticker, row in df_stocks.iterrows():
            print('{} / {} - Getting dividend yields for {}'.format(index, count, ticker))
            index = index + 1

            # Skip if already exist
            if (skip_if_exist):
                if not dividend_data.empty and ticker in dividend_data.index:
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
                        if (dividend_data.empty):
                            dividend_data = df_dividend
                        else:
                            dividend_data = dividend_data.combine_first(df_dividend)
                        dividend_data.to_csv(dividend_file, encoding='utf-8')
            except Exception as e:
                print('Ooops...error with {} - {}'.format(ticker, str(e)))
                continue


def main():
    """
    Main script.
    """

    stock_analysis = StockAnalysis()
    stock_analysis.fund_get_dividend_yields_for_exchange('KLS')


if __name__ == "__main__":
    main()
