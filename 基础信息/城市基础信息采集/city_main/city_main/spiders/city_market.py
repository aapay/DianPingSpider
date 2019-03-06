# -*- coding: utf-8 -*-
# 城市商圈采集
import scrapy
import json

from city_main.items import MarketsItem


class CitySpiderSpider(scrapy.Spider):
    name = 'city_market'

    # 单独配置pipelines
    custom_settings = {
        'ITEM_PIPELINES': {
            'city_main.pipelines.MarketsPipeline': 300,
        }
    }

    start_urls = ['http://www.dianping.com/citylist/']

    def parse(self, response):
        city_list = response.xpath('//*[@id="main"]/div[4]/ul/li')
        for c_item in city_list:
            i_list = c_item.xpath('./div[2]/div/a')
            for i in i_list:
                city = i.xpath('./text()').extract_first()
                href = i.xpath('./@href').extract_first()
                href = 'https://' + href[2:]
                item = MarketsItem()
                yield scrapy.Request(url=href, callback=self.parse_content, meta={'item': item, 'city': city})

    def parse_content(self, response):
        """
        处理城市列表
        """
        item = response.meta.get('item')
        city = response.meta.get('city')
        href = response.xpath('//*[@id="cata-hot"]/div/div/a/@href').extract_first()

        # 处理字符串 把闲杂符号去掉
        city_href = 'https:' + href

        yield scrapy.Request(url=city_href, callback=self.parse_city, meta={'item': item, 'city': city})

    def parse_city(self, response):
        """
        处理街镇列表
        :param response:
        :return:
        """
        api_url = 'http://api.map.baidu.com/geocoder/v2/?address=%s&output=json&ak=5f7my8MjAU4HFtO6ZpdazTQI1xKMwn2l'
        item = response.meta.get('item')
        city = response.meta.get('city')
        county_dl_list = response.xpath('//*[@id="J-shopall"]/div/div[2]/dl')
        for county_dl in county_dl_list:
            county = county_dl.xpath('./dt/a/text()').extract_first()

            county_li_list = county_dl.xpath('./dd/ul/li')
            if county_li_list:
                for county_li in county_li_list:
                    info = county_li.xpath('./a/text()').extract_first()
                    url = api_url % (city + county + info)
                    yield scrapy.Request(url=url, callback=self.parse_location, meta={'item': item, 'city':city, 'county':county,'district':info})
            else:
                # 没有三级街道
                url = api_url % (response.meta.get('city') + county)
                yield scrapy.Request(url=url, callback=self.parse_location, meta={'item': item, 'city':city, 'county':county,'district':''})

    def parse_location(self, response):
        data = json.loads(response.text)
        # 处理字符串 把闲杂符号去掉
        if data.get('status') == 0:
            item = response.meta.get('item')
            item['city'] = response.meta.get('city')
            item['county'] = response.meta.get('county')
            item['district'] = response.meta.get('district')
            item['lng'] = data.get('result').get('location').get('lng')
            item['lat'] = data.get('result').get('location').get('lat')
            item['comprehension'] = data.get('result').get('comprehension')
            item['city_level'] = data.get('result').get('level')

            yield item
