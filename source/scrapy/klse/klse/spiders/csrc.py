# -*- coding: utf-8 -*-
#
# Get the stock quotes

import os
import string

import pandas as pd
import scrapy

from scrapy import FormRequest

class CsrcSpider(scrapy.Spider):
    name = "csrc"

    _URL_BASE = 'http://www.csrc.gov.cn/newsite/'

    _SEARCH_TERM = '陈俊'

    def start_requests(self):
        urls = [self._URL_BASE]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        print("Posting the search term")
        return scrapy.FormRequest.from_response(
            response,
            formname='simsearch',
            formid='simsearch',
            formdata={'schword': self._SEARCH_TERM},
            callback=self.after_search
        )

    def after_search(self, response):
        print('Parsing the search result')
        print(response.body)


