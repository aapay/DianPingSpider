# -*- coding: utf-8 -*-
import scrapy

from markets.items import MarketsItem


class CitySpiderSpider(scrapy.Spider):
    name = 'city_spider'
    start_urls = ['http://api.map.baidu.com/geocoder/v2/?address=%E6%9F%98%E5%9F%8E%E5%8E%BF%E8%B5%B7%E5%8F%B0%E9%95%87&output=json&ak=5f7my8MjAU4HFtO6ZpdazTQI1xKMwn2l']

    def parse(self, response):
        # 读取数据库 地址名

        # 递归获取
        item = MarketsItem()
        yield scrapy.Request(url=href, callback=self.parse_content, meta={'item': item, 'city': city})

