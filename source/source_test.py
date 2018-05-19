"""
Tests for the source module.
"""

import unittest
import yahoofinance
import googlefinance


class SourceTest(unittest.TestCase):

    def test_get_stocks(self):
        print("Getting the stocks")