# -*- coding: utf-8 -*-


from zok.save.to_mysql import SaveToMysqlBase


class BasePipeline(SaveToMysqlBase):

    @staticmethod
    def get_sql(item):
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
        return sql


class LngAndLatPipeline(SaveToMysqlBase):
    """Lng and Lat line"""

    @staticmethod
    def get_sql(item):

        if item['data_type'] == 'market':
            sql = """INSERT INTO base_city_market_db(city, county, district, lng, lat, comprehension, city_level) VALUES ("{city}","{second}","{thirdly}","{lng}","{lat}","{comprehension}","{city_level}") """.format(
                city=item['city'],
                second=item['second'],
                thirdly=item['thirdly'],
                lng=item['lng'],
                lat=item['lat'],
                comprehension=item['comprehension'],
                city_level=item['city_level'],
            )
        elif item['data_type'] == 'landmark':
            sql = """INSERT INTO base_city_landmark_db(city, county, landmark, lng, lat, comprehension, city_level) VALUES ("{city}","{second}","{thirdly}","{lng}","{lat}","{comprehension}","{city_level}") """.format(
                city=item['city'],
                second=item['second'],
                thirdly=item['thirdly'],
                lng=item['lng'],
                lat=item['lat'],
                comprehension=item['comprehension'],
                city_level=item['city_level'],
            )
        elif item['data_type'] == 'school':
            sql = """INSERT INTO base_city_school_db(city, school, lng, lat, comprehension) VALUES ("{city}","{second}","{lng}","{lat}","{comprehension}") """.format(
                city=item['city'],
                second=item['second'],
                lng=item['lng'],
                lat=item['lat'],
                comprehension=item['comprehension'],
            )

        return sql

