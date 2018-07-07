#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""KLSE source from i3investor

Extract KLSE stock information from i3investor.

"""

import scrapy

class KLSESource(scrapy.Spider):
    """Getting KLSE market information"""

    start_urls = ['https://klse.i3investor.com/jsp/stocks.jsp']
    name = 'KLSE source'

    def parse(self, response):
        for title in response.css('h2.entry-title'):
            yield {'title': title.css('a ::text').extract_first()}

        for next_page in response.css('div.prev-post > a'):
            yield response.follow(next_page, self.parse)
