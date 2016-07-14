# -*-coding: utf-8 -*-

from scrapy.crawler import CrawlerProcess
#from scrapy.settings import Settings
from scrapy.conf import settings
from generic.model.config import DBSession
from generic.model.rule import Rule
from generic.spiders.Zzz import FromcsvSpider

# settings = Settings()
process = CrawlerProcess(settings)
db = DBSession()
rules = db.query(Rule).filter(Rule.enable == 1)
for rule in rules:
    process.crawl(FromcsvSpider, rule)
process.start()