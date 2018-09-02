# -*- coding: utf-8 -*-


from scrapy import cmdline


#cmdline.execute("scrapy crawl dividend_history".split())

# Grab the stock quotes
# cmdline.execute("scrapy crawl quotes".split())

# Grab dividends history
cmdline.execute("scrapy crawl dividend_history_malaysiastock".split())