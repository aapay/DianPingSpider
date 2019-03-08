# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BaseItem(scrapy.Item):
    data_type = scrapy.Field()  # 响应类型
    city = scrapy.Field()  # 主体城市
    second = scrapy.Field()  # 二级目录
    thirdly = scrapy.Field()  # 三级划分
