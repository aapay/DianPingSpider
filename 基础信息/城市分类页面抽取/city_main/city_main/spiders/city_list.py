# -*- coding: utf-8 -*-
import scrapy

from city_main.items import CityMainItem


class CityListSpider(scrapy.Spider):
    name = 'city_list'
    # allowed_domains = ['http://www.dianping.com/citylist']  # 仅允许该域名内
    start_urls = ['http://www.dianping.com/citylist/']

    def parse(self, response):
        city_list = response.xpath('//*[@id="main"]/div[4]/ul/li')
        for item in city_list:
            i_list = item.xpath('./div[2]/div/a')
            for i in i_list:
                city = i.xpath('./text()').extract_first()
                href = i.xpath('./@href').extract_first()
                href = 'https://' + href[2:]

                item = CityMainItem()
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
        item = response.meta.get('item')
        county_dl_list = response.xpath('//*[@id="J-shopall"]/div/div[2]/dl')
        for county_dl in county_dl_list:
            county = county_dl.xpath('./dt/a/text()').extract_first()

            county_li_list = county_dl.xpath('./dd/ul/li')
            district = ''
            for county_li in county_li_list:
                info = county_li.xpath('./a/text()').extract_first()
                district += info + ','

            # 处理字符串 把闲杂符号去掉
            item['city'] = response.meta.get('city')
            item['county'] = county
            item['district'] = district[:-1]

            yield item

