"""
=======================
Google Finance source
=======================
"""

import re
import requests
import time
from json import loads
from bs4 import BeautifulSoup
from yahoofinancials import YahooFinancials


class GoogleFinanceSource():
    """ Google Finance source """

    def __init__(self, ticker):
        print('constructor')


