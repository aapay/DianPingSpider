# -*- coding: utf-8 -*-
# __author__ = "zok" 
# Date: 2019/3/4  Python: 3.7
"""pip3 install fake-useragent"""
import requests
import pymysql

from fake_useragent import UserAgent

from config import *


class TargetSpider(object):
    ua = UserAgent(verify_ssl=False)

    def __init__(self, url):
        self.url = url

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
        response = requests.get(self.url, headers=headers)  # , proxies=proxies
        if response.status_code == 200:
            return response.text
        return None

    def parse_page(self):
        """解析"""
        from lxml import etree
        html = self.get_page
        etree = etree.HTML(html)

        # 列表城市解析
        city_list = etree.xpath('//*[@id="main"]/div[4]/ul/li')
        for item in city_list:
            i_list = item.xpath('./div[2]/div/a')
            for i in i_list:
                city = i.xpath('./text()')[0]
                href = i.xpath('./@href')[0]
                content = {'city': city, 'href': 'https://' + href[2:]}
                self.save_to_mysql(content)

    @staticmethod
    def save_to_mysql(content):
        db = pymysql.connect(host=HOST, user=USER, password=PASSWORD, db=DB_NAME, port=PORT)
        try:
            cur = db.cursor()
            sql_inset = """INSERT INTO city_list(city, href) VALUES ("%s","%s") """ % (content['city'], content['href'])
            cur.execute(sql_inset)
            db.commit()
        except Exception as e:
            print('错误回滚')
            db.rollback()
        finally:
            db.close()
