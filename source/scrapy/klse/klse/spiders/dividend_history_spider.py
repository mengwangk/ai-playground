# -*- coding: utf-8 -*-
#
# Get stock dividend history

import scrapy

class DividendHistorySpider(scrapy.Spider):
    name = "dividends"


    def start_requests(self):
        print("requests")


    def parse(self, response):
        print("parse")
