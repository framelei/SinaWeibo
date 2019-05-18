from scrapy import cmdline

# cmdline.execute('scrapy crawl news -s JOBDIR=crawls/storeMyRequest'.split())
cmdline.execute('scrapy crawl weibo'.split())