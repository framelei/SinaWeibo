from scrapy import cmdline

# cmdline.execute('scrapy crawl weibo -s JOBDIR=crawls/storeMyRequest'.split())
cmdline.execute('scrapy crawl weibo'.split())