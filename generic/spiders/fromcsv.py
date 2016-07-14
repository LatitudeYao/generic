# -*- coding: utf-8 -*-
import csv
import re

from generic.items import StoreLoader
from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.http import Request
from scrapy.item import Item,Field

class FromcsvSpider(CrawlSpider):
    name = "fromcsv"
    start_urls = ['http://news.china.com/']
    rules = (
        Rule(LinkExtractor(allow='http://news.china.com'), callback='parse_url'),
    )

    def parse_url(self,  response):
        with open(getattr(self, "file", "url.csv"), "rU") as f:
            # 以文件第一行作为字典的key,
            reader = csv.DictReader(f)
            for line in reader:
                if line.pop('name') == 'ChinaNews':
                    regex = line.pop('regex')
                    rex = re.compile(regex)
                    match = rex.match(response.url)
                    if match is not None:
                        yield Request(url=match.group(), callback=self.parse_content, dont_filter=True,
                                      meta={'field': line})

    def parse_content(self, response):
        item = Item()
        I = StoreLoader(item=item, response=response)
        for name, xpath in response.meta['field'].iteritems():
            if xpath:
                # 动态创建一个item
                item.fields[name] = Field()
                I.add_xpath(name, xpath)
            else:
                print '请添加对应的匹配规则！'
        yield I.load_item()
