# -*- coding: utf-8 -*-
# __author__ = "zok" 
# Date: 2019/3/5  Python: 3.7

"""
储存错误URL提供调用
"""
import pymysql
import re

from zok.zok_config import *


class ErrorUrl(object):
    """
    参数1 报错的url
    参数2 该项目的table名
    """
    db = pymysql.Connect(
        host=HOST,
        port=PORT,
        user=USER,
        password=PASSWORD,
        db=DB_NAME,
    )

    con = db.cursor()  # 创建游标

    def __init__(self, url, spider_name):
        self.url = url
        self.spider_name = spider_name

        if self.table_exists():
            self.create_table()

    def table_exists(self):
        # 这个函数用来判断表是否存在
        sql = "show tables;"
        self.con.execute(sql)
        tables = [self.con.fetchall()]
        table_list = re.findall('(\'.*?\')', str(tables))
        table_list = [re.sub("'", '', each) for each in table_list]
        if 'error_url' in table_list:
            return True
        else:
            return False

    def create_table(self):
        sql = """
          CREATE TABLE error_url (
          `id` int(20) NOT NULL AUTO_INCREMENT,
          spider VARCHAR(20),
          url VARCHAR(200),
          PRIMARY KEY (`id`)
          )character set utf8;"""
        self.con.execute(sql)  # 创建表

    def save_to_mysql(self):
        # 写sql语句 插数据，没有表的话要先在数据库创建
        sql = """INSERT INTO error_url(spider, url) VALUES ("%s","%s") """ % (self.spider_name, self.url)
        # 提交事务
        try:
            self.con.execute(sql)
            self.db.commit()
        except Exception as e:
            print(e)
            print('异常回滚')
            self.db.rollback()
        finally:
            """断开链接"""
            self.con.close()
            self.db.close()


