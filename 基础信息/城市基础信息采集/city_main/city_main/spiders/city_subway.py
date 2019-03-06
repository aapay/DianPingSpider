# -*- coding: utf-8 -*-
import scrapy
# 地铁沿线


class CitySubwaySpider(scrapy.Spider):
    name = 'city_subway'
    allowed_domains = ['www.baidu.com']
    start_urls = ['http://www.baidu.com/']

    def parse(self, response):
        pass
