# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from scrapy.conf import settings

class GenericPipeline(object):
    def process_item(self, item, spider):
        return item

class MongoPipeline(object):

    def __init__(self):
        port = settings['MONGODB_PORT']
        host = settings['MONGODB_HOST']
        dbname = settings['MONGODB_DBNAME']
        server = pymongo.MongoClient(port= port, host= host)
        db = server[dbname]
        self.db = db[settings['MONGODB_DOCNAME']]
        print 'aaaaaaaaa'

    def process_item(self, item, spider):
        item = dict(item)
        self.db.insert(item)
        return item