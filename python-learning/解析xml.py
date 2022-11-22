#!/usr/bin/env python
#-*- coding:utf-8 -*-


# 解析网页XML
'''
<a href="/">python</a>

会产生3个事件：
    1.start_element事件，在读取<a href="/">时；
    2.char_data事件，在读取python时；
    3.end_element事件，在读取</a>时。
'''


import json
from urllib import request
from xml.parsers.expat import ParserCreate

# XML解析器
class DefaultSaxHandler(object):
    def __init__(self):
        self.current_data = ''
        self.city = ''
        self.forecast = []
        self.weather = {}

    def start_element(self, name, attrs):
        # print('sax:start_element: %s, attrs: %s' % (name, str(attrs)))
        self.current_data = name
        if name == 'city':
            self.city = attrs['name']

    def end_element(self, name):
        # print('sax:end_element: %s' % name)
        if name == 'forecast':
            self.forecast.append(self.weather)
            self.weather = {}
        self.current_data = ''

    def char_data(self, text):
        # print('sax:char_data: %s' % text)
        if self.current_data == 'date':
            self.weather['date'] = text
        elif self.current_data == 'high':
            self.weather['high'] = int(text)
        elif self.current_data == 'low':
            self.weather['low'] = int(text)

    def to_json(self):
        return {'city': self.city, 'forecast': self.forecast}

# 模拟XML数据
xml = r'''<?xml version="1.0"?>
<root>
    <city name='Beijing'>
        <forecast>
            <date>2017-11-17</date>
            <high>43</high>
            <low>26</low>           
        </forecast>
        <forecast>
            <date>2017-11-18</date>
            <high>41</high>
            <low>20</low>           
        </forecast>
        <forecast>
            <date>2017-11-19</date>
            <high>43</high>
            <low>19</low>           
        </forecast>
    </city>  
</root>
'''

def parseXml(xml_str):
    handler = DefaultSaxHandler()
    parser = ParserCreate()
    parser.StartElementHandler = handler.start_element
    parser.EndElementHandler = handler.end_element
    parser.CharacterDataHandler = handler.char_data
    parser.Parse(xml_str)
    return handler.to_json()
    # return json.dumps(handler.to_json(), sort_keys=True, indent=4)

# 获取网页XML文本
# URL = ?
# with request.urlopen(URL, timeout=4) as f:
#     data = f.read()
# result = parseXml(data.decode('utf-8'))
result = parseXml(xml)
print(result['city'])


# 解析结果
'''
{
    "city": "Beijing",
    "forecast": [
        {
            "date": "2017-11-17",
            "high": 43,
            "low": 26
        },
        {
            "date": "2017-11-18",
            "high": 41,
            "low": 20
        },
        {
            "date": "2017-11-19",
            "high": 43,
            "low": 19
        }
    ]
}
'''