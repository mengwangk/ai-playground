#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""KLSE source from i3investor

Extract KLSE stock information from i3investor.

"""

import scrapy


class QuoteExtractor(scrapy.Spider):
    name = "stock quotes extractor"
    start_urls = [
        'https://klse.i3investor.com/jsp/stocks.jsp?g=S&m=int&s=Y',
    ]

    def parse(self, response):
        print("parsing----------------")
        for quote in response.css('#tablebody > tr.odd'):
            print("-----------------" + quote)

        # next_page = response.css('li.next a::attr("href")').extract_first()
        # if next_page is not None:
        #    yield response.follow(next_page, self.parse)
