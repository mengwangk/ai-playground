# -*- coding: utf-8 -*-
#
# Get stocks financial information

import scrapy


class FinancialsSpider(scrapy.Spider):
    """Stock financials scraper"""

    name = "financials"

    _URL_BASE = "https://klse.i3investor.com/servlets/stk/{}.jsp"

    def start_requests(self):
        urls = []
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = 'quotes-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)
