from selenium import webdriver
from scrapy.http import HtmlResponse
import time

class JavaScriptMiddleware(object):

    def process_request(self, request, spider):
        print "PhantomJS is starting..."
        driver = webdriver.PhantomJS('/Users/ForkEyes/phantomjs/bin/phantomjs')
        driver.get(request.url)
        time.sleep(1)
        body = driver.page_source
        # driver.close()
        return HtmlResponse(driver.current_url, body=body, encoding='utf-8', request=request)
