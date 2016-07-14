# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html


from scrapy.loader import ItemLoader
from scrapy.loader.processors import Compose


class StoreLoader(ItemLoader):
    #default_output_processor = Compose(lambda v: v[0], unicode.strip())

    # def title_in(self, value):
    #     for v in value:
    #         yield 'my name is' + v

    pass