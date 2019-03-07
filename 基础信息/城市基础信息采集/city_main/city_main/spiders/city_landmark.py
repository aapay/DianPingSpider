# -*- coding: utf-8 -*-
# # 给储备好的 landmark——list 追加坐标

import scrapy
import json

from city_main.items import LandmarkListItem


class CityLandmarkSpider(scrapy.Spider):

    name = 'city_landmark'

    # 单独配置pipelines
    custom_settings = {
        'ITEM_PIPELINES': {
            'city_main.pipelines.CityLandmarkPipeline': 300,
        },
        'DOWNLOADER_MIDDLEWARES': {
            'city_main.middlewares.CityMainDownloaderMiddleware': 10,
            'zok.random_UA.ua_random.RandomUserAgentMiddleware': 20,
        },
        'RANDOMIZE_DOWNLOAD_DELAY': True,
        'CONCURRENT_REQUESTS': 50,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 50,
        'CONCURRENT_REQUESTS_PER_IP': 50
    }

    start_urls = ['http://www.dianping.com/citylist']

    def parse(self, response):
        item = LandmarkListItem()
        # 导出city_landmark_list数据表 为txt然后逐行读取，并提交获取返回值
        url = 'http://api.map.baidu.com/geocoder/v2/?address=%s&output=json&ak=5f7my8MjAU4HFtO6ZpdazTQI1xKMwn2l'
        # 先判断是否有之前的错误链接
        with open('base_city_landmark_list.txt', 'r', encoding='utf-8') as f:
            text_lines = f.readlines()
            for line in text_lines:
                line = line.strip()
                line_list = line.split('\t')
                address = eval(line_list[0])+eval(line_list[1])+eval(line_list[2])
                attr_url = url % address
                yield scrapy.Request(url=attr_url, callback=self.parse_location, meta={'item': item, 'city': eval(line_list[0]), 'county': eval(line_list[1]), 'landmark': eval(line_list[2])})

    def parse_location(self, response):
        """清洗数据"""
        data = json.loads(response.text)
        # 处理字符串 把闲杂符号去掉
        if data.get('status') == 0:
            item = response.meta.get('item')
            item['city'] = response.meta.get('city')
            item['county'] = response.meta.get('county')
            item['landmark'] = response.meta.get('landmark')
            # 坐标
            item['lng'] = data.get('result').get('location').get('lng')
            item['lat'] = data.get('result').get('location').get('lat')
            item['comprehension'] = data.get('result').get('comprehension')
            item['city_level'] = data.get('result').get('level')

            yield item
        else:
            print('坐标获取失败')

