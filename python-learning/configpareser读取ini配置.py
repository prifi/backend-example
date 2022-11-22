#!usr/bin/env python
# -*- coding:utf-8 -*-
"""
@version:
author:fly
@time: 2022/04/15
@file: configpareser读取ini配置.py
@function:
@modify:
"""
from configparser import ConfigParser

# 写入配置
conf = ConfigParser()
conf['ES'] = {
    'host': '172.22.0.37',
    'port': '9200',
    'name': '',
    'password': '',
    'is_ssl': False
}

conf['SITE'] = {}
conf['SITE']['bl'] = 'bellelily'
conf['SITE']['fs'] = 'fairyseason'

with open('config.ini', 'w') as f:
    conf.write(f)

# 读取配置
conf = ConfigParser()
conf.read('config.ini')
print('ES' in conf)      # 是否在section中 True
print(conf.sections())   # 读取section ['ES', 'SITE']

# 获取特定的section
items = conf.items('SITE')   # [('bl', 'bellelily'), ('fs', 'fairyseason')]
print(dict(items))  # 转换成字典

# for k,v in conf['ES'].items():  # 遍历
#     print(v)

# 还原成python数据类型
type(conf['ES'].getboolean('is_ssl'))   # getint, getfloat

try:
    print(conf.get('ES',option='por'))
except Exception as e:
    print(e)   # No option 'por' in section: 'ES'