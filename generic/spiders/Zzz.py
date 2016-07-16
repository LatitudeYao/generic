# -*- coding: utf-8 -*-
import scrapy

from generic.items import StoreLoader, ZzhItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.http import Request
from scrapy.selector import Selector


class FromcsvSpider(scrapy.Spider):
    name = "test"

    def __init__(self, rule):
        self.rule = rule
        self.name = rule.name
        self.allowed_domains = rule.allow_domains.split(",")
        self.start_urls = rule.start_urls.split(",")
        super(FromcsvSpider,self).__init__()

    def parse(self, response):
        selector = Selector(response)
        # 提取当前页面通知的标题,时间,网址
        for sel in selector.xpath(self.rule.extract_from):
            I = StoreLoader(item=ZzhItem(), response=sel)
            # I.add_xpath('title',)
            ex_data = sel.xpath(self.rule.title_xpath).extract()
            title = ex_data[0] if len(ex_data) > 0 else ''
            ex_data = sel.xpath(self.rule.publish_time_xpath).extract()
            time = ex_data[0] if len(ex_data) > 0 else ''
            ex_data = sel.xpath(self.rule.source_site_xpath).extract()
            link = ex_data[0] if len(ex_data) > 0 else ''

            url = response.urljoin(link)
            I.add_value('title', title)
            I.add_value('time', time)
            I.add_value('url', url)
            yield Request(url, callback=self.parse_content, meta={'field': I})
            yield I.load_item()

        # 爬取下一页链接
        if selector.xpath(self.rule.next_page).extract():
            next_page = response.urljoin(selector.xpath(self.rule.next_page).extract()[0])
            yield Request(next_page, callback=self.parse)
        else:
            print '当前网址已经爬取完毕'

    def parse_content(self, response):
        I = response.meta['field']
        sel = Selector(response).xpath('//div[@id="content_body"]')
        if sel.xpath('string(.)').extract():
            content = sel.xpath('string(.)').extract()[0]
            I.add_value('content', content)
        else:
            print '这篇文章的xpath不一样'
        yield I.load_item()




