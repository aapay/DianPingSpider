# -*- coding: utf-8 -*-
# __author__ = "zok"
# Date: 2019/3/5  Python: 3.7

from zok.save.to_mysql import SaveToMysqlBase


class CityMainPipeline(SaveToMysqlBase):
    """
    全国城市三级联动
    """
    @staticmethod
    def get_sql(item):
        sql = """INSERT INTO base_city(city, county, district) VALUES ("%s","%s","%s") """ % (
        item['city'], item['county'], item['district'])
        return sql


class MarketsPipeline(SaveToMysqlBase):
    """
    全国【商圈】+【坐标】
    """
    @staticmethod
    def get_sql(item):
        sql = """INSERT INTO base_city_market(city, county, district, lng, lat, comprehension, city_level) VALUES ("%s","%s","%s","%s","%s","%s","%s") """ % (
        item['city'], item['county'], item['district'], item['lng'], item['lat'], item['comprehension'],
        item['city_level'])

        return sql


class CityLandmarkPipeline(SaveToMysqlBase):
    """
    城市【地标】-【坐标】
    """
    @staticmethod
    def get_sql(item):
        sql = """INSERT INTO base_city_landmark(city, county, landmark, lng, lat, comprehension, city_level) VALUES ("%s","%s","%s","%s","%s","%s","%s") """ % (
        item['city'], item['county'], item['landmark'], item['lng'], item['lat'], item['comprehension'],
        item['city_level'])

        return sql


class CityLandmarkListPipeline(SaveToMysqlBase):
    """
    城市地标列表信息【不含坐标】
    """
    @staticmethod
    def get_sql(item):
        sql = """INSERT INTO base_city_landmark(city, county, landmark) VALUES ("{city}","{county}","{landmark}") """.format(
            city=item['city'],
            county=item['county'],
            landmark=item['landmark'],
        )
        return sql

