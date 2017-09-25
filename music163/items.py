# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Music163Item(scrapy.Item):
    _id = scrapy.Field()
    name = scrapy.Field()
    url = scrapy.Field()
    movie = scrapy.Field()
    singer = scrapy.Field()
    album = scrapy.Field()
    album_url = scrapy.Field()
    comments = scrapy.Field()


class Music163SingerItem(scrapy.Item):
    _id = scrapy.Field()
    singer = scrapy.Field()
    headimg = scrapy.Field()
    info_url = scrapy.Field()
