# -*- coding: utf-8 -*-
import scrapy

from base.items import BaseItem


class BaseCitySpider(scrapy.Spider):
    name = 'base_city'
    start_urls = ['https://www.dianping.com/citylist']

    custom_settings = {
        'ITEM_PIPELINES': {
            'base.pipelines.BasePipeline': 300,
        },
        'DOWNLOADER_MIDDLEWARES': {
            'zok.random_UA.ua_random.RandomUserAgentMiddleware': 20,
            'zok.proxies.proxies.ProxyMiddleware': 15,
        },
        'RANDOMIZE_DOWNLOAD_DELAY': True,
        'CONCURRENT_REQUESTS': 5,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 5,
        'CONCURRENT_REQUESTS_PER_IP': 5
    }

    def parse(self, response):
        """parse CityList"""
        # type save
        city_list = response.xpath('//*[@id="main"]/div[4]/ul/li')
        for item in city_list:
            i_list = item.xpath('./div[2]/div/a')
            for i in i_list:
                city = i.xpath('./text()').extract_first()
                href = i.xpath('./@href').extract_first()
                href = 'https://' + href[2:]

                yield scrapy.Request(url=href, callback=self.parse_city_homepage, meta={'city': city})

    def parse_city_homepage(self, response):
        """homepage"""
        city = response.meta.get('city')
        href = response.xpath('//*[@id="cata-hot"]/div/div/a/@href').extract_first()
        if not href:
            with open('error/error_url.txt', 'a', encoding='utf-8') as f:
                f.write(city+','+response.url + '\n')
        else:
            # 处理字符串 把闲杂符号去掉
            city_href = 'https:' + href
            yield scrapy.Request(url=city_href, callback=self.parse_city, meta={'city': city})

    @ staticmethod
    def parse_city(response):
        """city"""
        item = BaseItem()

        """base"""
        base_dl_list = response.xpath('//*[@id="J-shopall"]/div/div[2]/dl')
        for base_dl in base_dl_list:
            second = base_dl.xpath('./dt/a/text()').extract_first()

            second_li_list = base_dl.xpath('./dd/ul/li')
            thirdly = ''
            for second_li in second_li_list:
                info = second_li.xpath('./a/text()').extract_first()
                thirdly += info + ','

            item['data_type'] = 'base'
            item['city'] = response.meta.get('city')
            item['second'] = second
            item['thirdly'] = thirdly[:-1]

            yield item

        """city_market"""
        market_dl_list = response.xpath('//*[@id="J-shopall"]/div/div[2]/dl')
        for market_dl in market_dl_list:
            second = market_dl.xpath('./dt/a/text()').extract_first()

            second_li_list = market_dl.xpath('./dd/ul/li')
            if second_li_list:
                for second_li in second_li_list:
                    info = second_li.xpath('./a/text()').extract_first()
                    item['data_type'] = 'market'
                    item['city'] = response.meta.get('city')
                    item['second'] = second
                    item['thirdly'] = info

                    yield item
            else:
                item['data_type'] = 'market'
                item['city'] = response.meta.get('city')
                item['second'] = second
                item['thirdly'] = ''

                yield item

        """city_landmark"""
        landmark_dl_list = response.xpath('//*[@id="J-shopall"]/div/div[3]/dl')
        for landmark_dl in landmark_dl_list:
            second = landmark_dl.xpath('./dt/a/text()').extract_first()

            second_li_list = landmark_dl.xpath('./dd/ul/li')
            for second_li in second_li_list:
                info = second_li.xpath('./a/text()').extract_first()
                item['data_type'] = 'landmark'
                item['city'] = response.meta.get('city')
                item['second'] = second
                item['thirdly'] = info

                yield item

        """city subway"""
        landmark_dl_list = response.xpath('//*[@id="J-shopall"]/div/div[4]/dl')
        for landmark_dl in landmark_dl_list:
            subway_numb = landmark_dl.xpath('./dt/a/text()').extract_first()
            second_li_list = landmark_dl.xpath('./dd/ul/li')
            for second_li in second_li_list:
                station = second_li.xpath('./a/text()').extract_first()
                item['data_type'] = 'subway'
                item['city'] = response.meta.get('city')
                item['second'] = subway_numb
                item['thirdly'] = station

                yield item

        """city school"""
        school_a_list = response.xpath('//*[@id="J-shopall"]/div/div[5]/ul/li')
        for school_a in school_a_list:
            school = school_a.xpath('./a/text()').extract_first()
            if school:
                item['data_type'] = 'school'
                item['city'] = response.meta.get('city')
                item['second'] = school
                item['thirdly'] = ''

                yield item

        """city hot"""
        hot_dl_list = response.xpath('//*[@id="J-shopall"]/div/div[1]/dl')
        for hot_dl in hot_dl_list:
            second = hot_dl.xpath('./dt/a/text()').extract_first()
            second_li_list = hot_dl.xpath('./dd/ul/li')
            thirdly = ''
            for second_li in second_li_list:
                info = second_li.xpath('./a/text()').extract_first()
                thirdly += info + ','

            item['data_type'] = 'hot'
            item['city'] = response.meta.get('city')
            item['second'] = second
            item['thirdly'] = thirdly[:-1]

            yield item

