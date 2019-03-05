# -*- coding: utf-8 -*-
# __author__ = "zok" 
# Date: 2019/3/4  Python: 3.7
"""pip3 install fake-useragent"""
import requests
import pymysql
import hashlib
import redis

from fake_useragent import UserAgent

from config import *
from proxies.proxies import proxies


class TargetSpider(object):
    ua = UserAgent(verify_ssl=False)
    host = HOST
    user = USER
    password = PASSWORD
    db_name = DB_NAME
    port = PORT
    redis_db = REDIS_DB
    r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=redis_db)

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
        response = requests.get(self.url, headers=headers, proxies=proxies)
        if response.status_code == 200:
            return response.text
        return None

    @property
    def parse_administrative_division(self):
        """行政区域信息抓取（不含坐标）"""
        from lxml import etree
        html = self.get_page
        if not html:
            print('页面获取失败,跳过当前城市')
            return True
        etree = etree.HTML(html)
        city = etree.xpath('//*[@id="logo-input"]/div/a[2]/span[2]/text()')
        if not city:
            return False
        city = city[0]
        # print('当前采集地区', city)
        dl_list = etree.xpath('//*[@id="J-shopall"]/div/div[2]/dl')
        for dl in dl_list:  # ./从dl开始取
            district = dl.xpath('./dt/a/text()')[0]
            li_list = dl.xpath('./dd/ul/li')
            address = ''
            for li in li_list:
                address += li.xpath('./a/text()')[0] + ','
            content = {"city": city, 'district': district, 'address': address[:-1]}
            self.save_to_mysql_administrative_division(content)
        return True

    def save_to_mysql_administrative_division(self, content):
        """行政区域储存"""
        db = pymysql.connect(host=self.host, user=self.user,
                             password=self.password, db=self.db_name, port=self.port)
        cur = db.cursor()
        sql_inset = """INSERT INTO administrative_division(city, district, address) VALUES ("%s","%s","%s") """ % (
            content['city'], content['district'], content['address'])
        try:
            # 取出城市+省份的hash作为redis更新参数
            text_hash = self.get_md5(content['city'] + content['district'])
            if self.r.exists(text_hash):
                # 取出街道如果不同就更新、相同则不操作
                info_id = int(self.r.get(text_hash))
                sql_select = """select address from administrative_division where id=%s""" % info_id
                cur.execute(sql_select)
                data = cur.fetchone()
                if data[0] == content['address']:
                    return
                # 更新
                sql_update = """UPDATE administrative_division SET district='%s' WHERE id=%s;""" % (content['address'], info_id)
                cur.execute(sql_update)
                print('部分更新', info_id)
            else:
                # 插入
                cur.execute(sql_inset)
                self.r.set(text_hash, int(db.insert_id()))  # 传入redis，更新储备
            db.commit()
        except Exception as e:
            print('错误回滚')
            db.rollback()
        finally:
            db.close()

    @staticmethod
    def get_md5(data_txt):
        """md5 唯一值校验"""
        h = hashlib.md5()
        h.update(data_txt.encode('utf-8'))
        return h.hexdigest()

