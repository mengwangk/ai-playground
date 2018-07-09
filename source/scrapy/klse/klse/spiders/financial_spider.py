# -*- coding: utf-8 -*-
#
# Get the stock financial


import scrapy


class FinancialSpider(scrapy.Spider):
    name = "financial"

    def start_requests(self):
        print("requests")

    def parse(self, response):
        print("parse")
