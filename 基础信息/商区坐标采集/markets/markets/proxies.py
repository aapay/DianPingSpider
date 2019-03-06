# -*- coding: utf-8 -*-
# __author__ = "zok" 
# Date: 2019/3/5  Python: 3.7

import base64

# 代理服务器
proxyServer = "http://http-dyn.abuyun.com:9020"

# 代理隧道验证信息
proxyUser = "H926E120746I0YID"
proxyPass = "0506E6770F57EB6B"

proxyAuth = "Basic " + base64.urlsafe_b64encode(bytes((proxyUser + ":" + proxyPass), "ascii")).decode("utf8")
