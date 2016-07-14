# -*- coding: utf-8 -*-

import re

from generic.items import StoreLoader
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.http import Request,HtmlResponse
from scrapy.item import Item, Field


class FromcsvSpider(CrawlSpider):
    name = "test"

    def __init__(self, rule):
        self.rule = rule
        self.name = rule.name
        self.allowed_domains = rule.allow_domains.split(",")
        self.start_urls = rule.start_urls.split(",")
        rule_list = []
        # 添加下一页规则
        if rule.next_page:
            rule_list.append(Rule(LinkExtractor(restrict_xpaths= rule.next_page)))
        # 添加抽取文章链接的规则
        rule_list.append(Rule(LinkExtractor(
            allow= [rule.allow_url],
            restrict_xpaths= [rule.extract_from],),
            callback = self.parse_content))
        self.rules = tuple(rule_list)
        super(FromcsvSpider,self).__init__()

    def parse_content(self, response):
        item = Item()
        I = StoreLoader(item=item, response=response)
        # for name, xpath in response.meta['field'].iteritems():
        #     if xpath:
        #         # 动态创建一个item
        #         item.fields[name] = Field()
        #         I.add_xpath(name, xpath)
        #     else:
        #         print '请添加对应的匹配规则！'
        item.fields['title'] = Field()
        I.add_xpath('title', self.rule.title_xpath)
        yield I.load_item()




