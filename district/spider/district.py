# -*- coding: utf-8 -*-
# __author__ = "zok"
# Date: 2019/3/4  Python: 3.7
"""pip3 install fake-useragent"""
import requests
import pymysql

from fake_useragent import UserAgent

from proxies.proxies import proxies
from config import *


class TargetSpider(object):
    ua = UserAgent(verify_ssl=False)

    def __init__(self, pre_city, url):
        self.url = url
        self.pre_city = pre_city

    def get_random_ua(self):
        """get random ua"""
        headers = {
            'User-Agent': self.ua.random,
        }
        return headers

    @property
    def get_page(self):
        """return text"""
        headers = self.get_random_ua()
        response = requests.get(self.url, headers=headers, proxies=proxies)
        if response.status_code == 200:
            return response.text
        return None

    def parse_page(self):
        """解析"""
        from lxml import etree
        html = self.get_page
        etree = etree.HTML(html)
        # 行政区域解析
        district_list = etree.xpath('//*[@id="region-nav"]')
        print(district_list)
        address = ''
        for district in district_list:
            add = district.xpath('./span/text()')[0]
            address += add

        print(address[:-1])
        # self.save_to_mysql(address[:-1])

    def save_to_mysql(self, content):
        """储存地址"""
        db = pymysql.connect(host=HOST, user=USER, password=PASSWORD, db=DB_NAME, port=PORT)
        try:
            cur = db.cursor()
            sql_inset = """INSERT INTO district_db(city, district) VALUES ("%s","%s") """ % (self.pre_city, content)
            cur.execute(sql_inset)
            db.commit()
        except Exception as e:
            print('错误回滚')
            db.rollback()
        finally:
            db.close()
