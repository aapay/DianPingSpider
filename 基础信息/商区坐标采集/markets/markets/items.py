# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MarketsItem(scrapy.Item):
    title = scrapy.Field()
    lng = scrapy.Field()
    lat = scrapy.Field()
    comprehension = scrapy.Field()
    city_level = scrapy.Field()


