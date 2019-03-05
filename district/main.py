# -*- coding: utf-8 -*-
# __author__ = "zok" 
# Date: 2019/3/4  Python: 3.7
import pymysql

from spider import district
from config import *

if __name__ == '__main__':
    """start"""
    # 1.获取城市+链接
    db = pymysql.connect(host=HOST, user=USER, password=PASSWORD, db=DB_NAME, port=PORT)
    cur = db.cursor()
    sql = "select * from city_list"
    try:
        cur.execute(sql)  # 执行sql语句
        results = cur.fetchall()  # 获取查询的所有记录
        # 遍历结果
        for row in results:
            city = row[1]
            url = row[2]
            visit = district.TargetSpider(city, url)
            visit.parse_page()

    except Exception as e:
        raise e
    finally:
        db.close()  # 关闭连接






