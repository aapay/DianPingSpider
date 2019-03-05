# -*- coding: utf-8 -*-
# __author__ = "zok" 
# Date: 2019/3/4  Python: 3.7
import requests

from config import *

# 要访问的目标页面
targetUrl = "http://test.abuyun.com"


# 代理服务器
proxyHost = "http-dyn.abuyun.com"
proxyPort = "9020"

# 代理隧道验证信息
proxyUser = PROXYUSER
proxyPass = PROXYPASS

proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
    "host": proxyHost,
    "port": proxyPort,
    "user": proxyUser,
    "pass": proxyPass,
}

proxies = {
    "http": proxyMeta,
    "https": proxyMeta,
}
