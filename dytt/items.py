# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DyttItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    cover = scrapy.Field()
    screenshot = scrapy.Field()
    name = scrapy.Field()
    city = scrapy.Field()
    category = scrapy.Field()
    director = scrapy.Field()
    actors = scrapy.Field()
    profile = scrapy.Field()
