# -*- coding: utf-8 -*-
import pymysql

# mysql
HOST = "localhost"
USER = "root"
PASSWORD = ""
DB_NAME = "dianping"
PORT = 3306


class CityMainPipeline(object):
    conn = None
    cursor = None  # 游标对象

    # 1. 链接数据库
    # 2. 执行sql语句
    # 3. 提交

    # 爬虫开始执行
    def open_spider(self, spider):
        print('开始爬虫，链接数据库')
        self.conn = pymysql.Connect(
            host=HOST,
            port=PORT,
            user=USER,
            password=PASSWORD,
            db=DB_NAME,
        )

    # 对提交的item对象，mysql数据库储存
    # 爬虫每次提交item，该方法被执行一次
    def process_item(self, item, spider):

        # 写sql语句 插数据，没有表的话要先在数据库创建
        sql = """INSERT INTO base_city(city, county, district) VALUES ("%s","%s","%s") """ % (item['city'], item['county'], item['district'])

        # 创建游标对象
        self.cursor = self.conn.cursor()

        # 提交事务
        try:
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception as e:
            print(e)
            print('异常回滚')
            self.conn.rollback()

        return item

    # 结束爬虫时调用
    def close_spider(self, spider):
        print('爬虫结束, 关闭通道')
        self.cursor.close()
        self.conn.close()
