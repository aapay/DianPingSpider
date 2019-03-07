# -*- coding: utf-8 -*-
# __author__ = "zok" 
# Date: 2019/3/7  Python: 3.7

import pymysql

from zok.zok_config import *


class SaveToMysqlBase(object):
    """
    mysql储存基类
    新增语法 INSERT INTO 表名(city, county, district) VALUES ("%s","%s","%s")
    更新语法 UPDATE 表名 SET mail = "playstation.com" WHERE user_name = "Peter"
    """
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

    def process_item(self, item, spider):
        # 写sql语句 插数据，没有表的话要先在数据库创建

        # 创建游标对象
        sql = self.get_sql(item)
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
