# -*- coding: utf-8 -*-
import scrapy
import json

from base.items import BaseLngLatItem


class LngAndLatSpider(scrapy.Spider):
    name = 'lng_and_lat'
    start_urls = ['https://www.dianping.com/citylist']

    custom_settings = {
        'ITEM_PIPELINES': {
            'base.pipelines.LngAndLatPipeline': 300,
        },
        'DOWNLOADER_MIDDLEWARES': {
            'zok.random_UA.ua_random.RandomUserAgentMiddleware': 20,
        },
        'RANDOMIZE_DOWNLOAD_DELAY': True,
        'CONCURRENT_REQUESTS': 16,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 16,
        'CONCURRENT_REQUESTS_PER_IP': 16,
    }

    def parse(self, response):
        """
        逐表爬取，避免并发窜表
        check error url for error_url_info.txt
        :param response:
        :return:
        """

        item = BaseLngLatItem()
        with open('error/error_url_info.txt', 'r+', encoding='utf-8') as f:
            text_lines = f.readlines()
            print(text_lines)
            if text_lines == '':
                return False
            f.truncate()  # 清空文件
            for line in text_lines:
                line_list = line.split('|')
                attr_url = line_list[2].strip()
                address = line_list[1].split(',')
                get_type = line_list[0].strip()
                thirdly = ''
                if len(address) == 3:
                    thirdly = address[2]
                elif len(address) == 2:
                    thirdly = ''
                yield scrapy.Request(url=attr_url, callback=self.parse_location,
                                     meta={'type': get_type, 'item': item, 'city': address[0],
                                           'second': address[1],
                                           'thirdly': thirdly})

        url = 'http://api.map.baidu.com/geocoder/v2/?address={address}&output=json&ak=5f7my8MjAU4HFtO6ZpdazTQI1xKMwn2l'

        # with open('data/base_city_school.txt', 'r', encoding='utf-8') as f:
        #     text_lines = f.readlines()
        #     for line in text_lines:
        #         line = line.strip()
        #         line_list = line.split('\t')
        #         address = eval(line_list[0]) + eval(line_list[1])
        #         attr_url = url.format(address=address)
        #         yield scrapy.Request(url=attr_url, callback=self.parse_location,
        #                              meta={'type': 'school', 'item': item, 'city': eval(line_list[0]), 'second': eval(line_list[1]),
        #                                    'thirdly': ''})
        #
        # with open('data/base_city_landmark.txt', 'r', encoding='utf-8') as f:
        #     text_lines = f.readlines()
        #     for line in text_lines:
        #         line = line.strip()
        #         line_list = line.split('\t')
        #         address = eval(line_list[0]) + eval(line_list[1]) + eval(line_list[2])
        #         attr_url = url.format(address=address)
        #         yield scrapy.Request(url=attr_url, callback=self.parse_location,
        #                              meta={'type': 'landmark', 'item': item, 'city': eval(line_list[0]), 'second': eval(line_list[1]),
        #                                    'thirdly': eval(line_list[2])})
        #
        # with open('data/base_city_market.txt', 'r', encoding='utf-8') as f:
        #     text_lines = f.readlines()
        #     for line in text_lines:
        #         line = line.strip()
        #         line_list = line.split('\t')
        #         if len(line_list) == 3:
        #             address = eval(line_list[0]) + eval(line_list[1]) + eval(line_list[2])
        #             attr_url = url.format(address=address)
        #             yield scrapy.Request(url=attr_url, callback=self.parse_location,
        #                                  meta={'type': 'market', 'item': item, 'city': eval(line_list[0]), 'second': eval(line_list[1]),
        #                                        'thirdly': eval(line_list[2])})
        #         elif len(line_list) == 2:
        #             address = eval(line_list[0]) + eval(line_list[1])
        #             attr_url = url.format(address=address)
        #             yield scrapy.Request(url=attr_url, callback=self.parse_location,
        #                                  meta={'type': 'market', 'item': item, 'city': eval(line_list[0]), 'second': eval(line_list[1]),
        #                                        'thirdly': ''})

    @staticmethod
    def parse_location(response):
        """清洗数据"""
        data = json.loads(response.text)
        # 处理字符串 把闲杂符号去掉
        if data.get('status') == 0:
            item = response.meta.get('item')
            item['data_type'] = response.meta.get('type')
            item['city'] = response.meta.get('city')
            item['second'] = response.meta.get('second')
            item['thirdly'] = response.meta.get('thirdly')
            # 坐标
            item['lng'] = data.get('result').get('location').get('lng')
            item['lat'] = data.get('result').get('location').get('lat')
            item['comprehension'] = data.get('result').get('comprehension')
            item['city_level'] = data.get('result').get('level')

            yield item
        else:
            print('GET失败')
            data_type = response.meta.get('type')
            city = response.meta.get('city')
            second = response.meta.get('second')
            thirdly = response.meta.get('thirdly')
            if thirdly:
                info = city + "," + second + "," + thirdly
            else:
                info = city + "," + second
            with open('error/error_url_info.txt', 'a', encoding='utf-8') as f:
                f.write(data_type + '|' + info + '|' + response.url + '\n')

