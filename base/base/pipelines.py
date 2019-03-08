# -*- coding: utf-8 -*-

import pymysql

from zok.repetition.update_cache import CacheRedis

# mysql
MYSQL_HOST = "localhost"
MYSQL_USER = "root"
MYSQL_PASSWORD = ""
MYSQL_DB_NAME = "dianping"
MYSQL_PORT = 3306


class BasePipeline(object):
    conn = None
    cursor = None  # 游标对象
    redis = CacheRedis()

    def open_spider(self, spider):
        print('开始爬虫，链接数据库')
        self.conn = pymysql.Connect(
            host=MYSQL_HOST,
            port=MYSQL_PORT,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            db=MYSQL_DB_NAME,
        )

    def process_item(self, item, spider):
        # 写sql语句 插数据，没有表的话要先在数据库创建
        if item['data_type'] == 'base':
            sql = """INSERT INTO base_city(city, county, district) VALUES ("{city}","{second}","{thirdly}") """.format(
                city=item['city'],
                second=item['second'],
                thirdly=item['thirdly'],
            )
        elif item['data_type'] == 'market':
            sql = """INSERT INTO base_city_market(city, county, district) VALUES ("{city}","{second}","{thirdly}") """.format(
                city=item['city'],
                second=item['second'],
                thirdly=item['thirdly'],
            )
        elif item['data_type'] == 'landmark':
            sql = """INSERT INTO base_city_landmark(city, county, landmark) VALUES ("{city}","{second}","{thirdly}") """.format(
                city=item['city'],
                second=item['second'],
                thirdly=item['thirdly'],
            )
        elif item['data_type'] == 'subway':
            sql = """INSERT INTO base_city_subway(city, subway_num, station) VALUES ("{city}","{second}","{thirdly}") """.format(
                city=item['city'],
                second=item['second'],
                thirdly=item['thirdly'],
            )
        elif item['data_type'] == 'school':
            sql = """INSERT INTO base_city_school(city, school) VALUES ("{city}","{second}") """.format(
                city=item['city'],
                second=item['second'],
            )
        elif item['data_type'] == 'hot':
            sql = """INSERT INTO base_city_hot(city, hot_type, hot_key) VALUES ("{city}","{second}","{thirdly}") """.format(
                city=item['city'],
                second=item['second'],
                thirdly=item['thirdly'],
            )

        if not self.redis.redis_exists(sql):
            # 创建游标对象
            self.cursor = self.conn.cursor()
            # 提交事务
            try:
                self.cursor.execute(sql)
                last_id = int(self.conn.insert_id())  # 取最近插入的一条
                self.conn.commit()
                self.redis.save_redis(sql, last_id)
            except Exception as e:
                print(e)
                print('异常回滚')
                self.conn.rollback()
            return item
        else:
            # print('已有相同数据无需插入')
            pass

    def close_spider(self, spider):
        print('爬虫结束, 关闭通道')
        self.cursor.close()
        self.conn.close()


class LngAndLatPipeline(object):
    """Lng and Lat line"""
    conn = None
    cursor = None  # 游标对象
    redis = CacheRedis()

    def open_spider(self, spider):
        print('开始爬虫，链接数据库')
        self.conn = pymysql.Connect(
            host=MYSQL_HOST,
            port=MYSQL_PORT,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            db=MYSQL_DB_NAME,
        )

    def process_item(self, item, spider):
        # 写sql语句 插数据，没有表的话要先在数据库创建
        if item['data_type'] == 'market':
            sql = """INSERT INTO base_city_market(city, county, district) VALUES ("{city}","{second}","{thirdly}") """.format(
                city=item['city'],
                second=item['second'],
                thirdly=item['thirdly'],
            )
        elif item['data_type'] == 'landmark':
            sql = """INSERT INTO base_city_landmark(city, county, landmark) VALUES ("{city}","{second}","{thirdly}") """.format(
                city=item['city'],
                second=item['second'],
                thirdly=item['thirdly'],
            )
        elif item['data_type'] == 'subway':
            sql = """INSERT INTO base_city_subway(city, subway_num, station) VALUES ("{city}","{second}","{thirdly}") """.format(
                city=item['city'],
                second=item['second'],
                thirdly=item['thirdly'],
            )
        elif item['data_type'] == 'school':
            sql = """INSERT INTO base_city_school(city, school) VALUES ("{city}","{second}") """.format(
                city=item['city'],
                second=item['second'],
            )

        if not self.redis.redis_exists(sql):
            # 创建游标对象
            self.cursor = self.conn.cursor()
            # 提交事务
            try:
                self.cursor.execute(sql)
                last_id = int(self.conn.insert_id())  # 取最近插入的一条
                self.conn.commit()
                self.redis.save_redis(sql, last_id)
            except Exception as e:
                print(e)
                print('异常回滚')
                self.conn.rollback()
            return item
        else:
            # print('已有相同数据无需插入')
            pass

    def close_spider(self, spider):
        print('爬虫结束, 关闭通道')
        self.cursor.close()
        self.conn.close()


