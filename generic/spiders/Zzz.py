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
        '''提取当前页通知的时间,链接,标题,并且通过链接进入通知正文'''
        selector = Selector(response)
        # 提取当前页面通知的标题,时间,网址
        for sel in selector.xpath(self.rule.extract_from):
            I = StoreLoader(item=ZzhItem(), selector=sel, response=response)
            I.add_xpath('title', self.rule.title_xpath)
            I.add_xpath('time', self.rule.publish_time_xpath)
            # 获取通知链接,并进入正文部分
            link = sel.xpath(self.rule.source_site_xpath).extract()
            url = response.urljoin(link) if len(link) > 0 else '提取失败'
            I.add_value('url', url)
            yield Request(url, callback=self.parse_content, meta={'ItemLoader': I})
        # 抓取下一页链接
        if selector.xpath(self.rule.next_page).extract():
            next_page = response.urljoin(selector.xpath(self.rule.next_page).extract()[0])
            yield Request(next_page, callback=self.parse)
        else:
            print '当前网址已经爬取完毕'

    def parse_content(self, response):
        '''获取通知正文内容'''
        I = response.meta['ItemLoader']
        sel = Selector(response).xpath(self.rule.body_xpath)
        if sel.xpath('string(.)').extract():
            content = sel.xpath('string(.)').extract()[0]
            I.add_value('content', content)
        else:
            I.add_value('content', '提取失败')
            print '这篇文章的xpath不一样'
        yield I.load_item()




