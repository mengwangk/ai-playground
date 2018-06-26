"""
Tests for the fundamental module.
"""

import unittest
import datetime as dt

from fundamental import DividendYield


class FundamentalTest(unittest.TestCase):
    _TICKER = ['6742.KL','1155.KL', '4502.KL']
    _END_DATE = dt.datetime.today().strftime('%Y-%m-%d')
    _START_DATE = dt.date(dt.date.today().year - 5, 1, 1).strftime('%Y-%m-%d')

    def test_get_dividend_histories(self):
        dividend_yield = DividendYield(self._TICKER)
        dividend_yield.generate_history_file(file_name = 'dividend_yield', base_dir='../dataset');
