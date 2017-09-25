# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from scrapy.conf import settings
from .items import Music163Item
from .items import Music163SingerItem

class Music163Pipeline(object):
    def __init__(self):
        host = settings['MONGODB_HOST']
        port = settings['MONGODB_PORT']
        db_name = settings['MONGODB_DBNAME']
        self.client = pymongo.MongoClient(host=host, port=port)
        self.tdb = self.client[db_name]
        self.post = self.tdb[settings['MONGODB_DOCNAME_MUSICS']]

    def process_item(self, item, spider):
        '''先判断itme类型，在放入相应数据库'''
        if isinstance(item, Music163Item):
            try:
                music_info = dict(item)  #
                if self.post.insert(music_info):
                    print('Music Successful!')
            except Exception:
                pass
        if isinstance(item, Music163SingerItem):
            try:
                singer_info = dict(item)
                self.post = self.tdb[settings['MONGODB_DOCNAME_GESHOU']]
                if self.post.insert(singer_info):
                    print('Singer Successful!')
            except Exception:
                pass
        return item
