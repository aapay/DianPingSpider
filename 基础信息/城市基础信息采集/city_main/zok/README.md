# Zok组件使用说明

### 目录
- repetition 内容更新处理
- save 通用持久化存储组件
- 随机UA

**基于redis内容去重更新**
    

**mysql储存**
1. 必须在zok_config中配置要持久化的数据库账户密码
2. 在爬虫项目文件pipelines管道中，引入并使用
**必须调用 def_sql(item)方法，并返回sql语句即可**
```python
from zok.save.to_mysql import SaveToMysqlBase

class CityLandmarkListPipeline(SaveToMysqlBase):
    @staticmethod
    def get_sql(item):
        sql = """INSERT INTO base_city_landmark(city, county, landmark) VALUES ("{city}","{county}","{landmark}") """.format(
            city=item['city'],
            county=item['county'],
            landmark=item['landmark'],
        )
        return sql
```
**txt储存**


**随机UA**
```python
# setting.py中 加入即可
DOWNLOADER_MIDDLEWARES = {
   'zok.random_UA.ua_random.RandomUserAgentMiddleware': 20,
}
```

**代理ip设置**
```python
# 在setting中配置即可
DOWNLOADER_MIDDLEWARES = {
   'zok.proxies.proxies.ProxyMiddleware': 15,  # 自定义的中间件
}
```