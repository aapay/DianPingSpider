# -*- coding: utf-8 -*-
# __author__ = "zok" 
# Date: 2019/3/4  Python: 3.7

from spider import city_list

if __name__ == '__main__':
    """start"""
    # 获取城市
    visit = city_list.TargetSpider('http://www.dianping.com/citylist')
    visit.parse_page()




