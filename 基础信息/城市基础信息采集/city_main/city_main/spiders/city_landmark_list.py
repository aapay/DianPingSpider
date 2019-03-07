# -*- coding: utf-8 -*-
# __author__ = "zok"
# Date: 2019/3/5  Python: 3.7

# 用于获取基础地标数据，提供给后面坐标获取

import scrapy

from city_main.items import LandmarkListItem


class CityLandmarkListSpider(scrapy.Spider):

    name = 'city_landmark_list'
    start_urls = ['http://www.dianping.com/citylist']
    # 单独配置pipelines
    custom_settings = {
        'ITEM_PIPELINES': {
            'city_main.pipelines.CityLandmarkListPipeline': 300,
        },
    }

    def parse(self, response):
        item = LandmarkListItem()
        flag = False
        # 先判断是否有之前的错误链接，有的话就执行该方法内的
        with open('CityLandmarkListSpider_error_url.txt', 'r', encoding='utf-8') as f:
            flag = True
            while True:
                text_line = f.readline()
                if text_line:
                    error_info = text_line.split(',')
                    print('检测到有错误链接', error_info[1], error_info[0])
                    yield scrapy.Request(url=error_info[1], callback=self.parse_content, meta={'item': item, 'city': error_info[0]})
                else:
                    break
        if flag:
            print('错误链接补录完成')
            return

        # 正式操作
        city_list = response.xpath('//*[@id="main"]/div[4]/ul/li')
        for c_item in city_list:
            i_list = c_item.xpath('./div[2]/div/a')
            for i in i_list:
                city = i.xpath('./text()').extract_first()
                href = i.xpath('./@href').extract_first()
                href = 'https://' + href[2:]

                yield scrapy.Request(url=href, callback=self.parse_content, meta={'item': item, 'city': city})

    def parse_content(self, response):
        """
        处理城市列表
        """
        item = response.meta.get('item')
        city = response.meta.get('city')
        href = response.xpath('//*[@id="cata-hot"]/div/div/a/@href').extract_first()
        if not href:
            with open('CityLandmarkListSpider_error_url.txt', 'a', encoding='utf-8') as f:
                f.write(city+','+response.url + '\n')
        else:
            # 处理字符串 把闲杂符号去掉
            city_href = 'https:' + href
            yield scrapy.Request(url=city_href, callback=self.parse_city, meta={'item': item, 'city': city})

    def parse_city(self, response):
        """
        处理街镇列表
        :param response:
        :return:
        """
        item = response.meta.get('item')
        county_dl_list = response.xpath('//*[@id="J-shopall"]/div/div[3]/dl')
        if county_dl_list:
            for county_dl in county_dl_list:
                county = county_dl.xpath('./dt/a/text()').extract_first()
                county_li_list = county_dl.xpath('./dd/ul/li')
                for county_li in county_li_list:
                    info = county_li.xpath('./a/text()').extract_first()

                    item['city'] = response.meta.get('city')
                    item['county'] = county
                    item['landmark'] = info
                    yield item
