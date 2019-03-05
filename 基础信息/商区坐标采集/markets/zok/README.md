# Zok组件使用说明

### 目录
- error_url 
    
    1. 补漏功能
    2. 处理爬取失败的链接
    3. 将单个爬虫爬取失败的链接单独储存，在运行爬虫之前查询该错误链接是否有，如果有就只爬取库中的错误链接，否则重新爬取
    
- repetition

    内容更新处理
    
    
# 补漏使用方法
1. 配置组件 zok_config.py 的 数据库链接
2. 捕获错误rul并储存  中间件middlewares的process_exception方法中引入
```python
from zok.error_url import save_error

def process_exception(self, request, exception, spider):
    save_error.ErrorUrl(request.url, spider.name)
```