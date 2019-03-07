# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CityMainItem(scrapy.Item):
    city = scrapy.Field()
    county = scrapy.Field()
    district = scrapy.Field()


class MarketsItem(scrapy.Item):
    city = scrapy.Field()
    county = scrapy.Field()
    district = scrapy.Field()
    lng = scrapy.Field()
    lat = scrapy.Field()
    comprehension = scrapy.Field()
    city_level = scrapy.Field()


class LandmarkListItem(scrapy.Item):
    city = scrapy.Field()
    county = scrapy.Field()
    landmark = scrapy.Field()
    lng = scrapy.Field()
    lat = scrapy.Field()
    comprehension = scrapy.Field()
    city_level = scrapy.Field()


class LandmarkItem(scrapy.Item):
    city = scrapy.Field()
    county = scrapy.Field()
    landmark = scrapy.Field()
