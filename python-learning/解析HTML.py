#!/usr/bin/env python
#-*- coding: utf-8 -*-

from html.parser import HTMLParser
from html.entities import name2codepoint


'''
# xml test
<li>
    <h3 class="event-title"><a href="/events/python-events/1215/">PyCon LT 2022</a></h3>
    <p>         
        <time datetime="2022-05-26T00:00:00+00:00">26 May &ndash; 27 May <span class="say-no-more"> 2022</span></time>
        <span class="event-location">Vilnius, Lithuania</span>
    </p>
</li>

<li>
    <h3 class="event-title"><a href="/events/python-events/1103/">PyCon Italy 22</a></h3>
    <p>
         <time datetime="2022-06-02T00:00:00+00:00">02 June &ndash; 05 June <span class="say-no-more"> 2022</span></time>
        <span class="event-location">Florence, Italy</span>
    </p>
</li>
'''


'''
# 解析 HTML

from urllib import request
url = 'https://www.python.org/events/python-events/'
with request.urlopen(url, timeout=30) as f:
    data = f.read()
xml = data.decode('utf-8')

import re,json
from html.parser import HTMLParser
from html.entities import name2codepoint

class MyHTMLParser(HTMLParser):

    def __init__(self):
        super().__init__()
        self.__flag = ''
        self._time = ''
        self.info = []
        self.data = {}

    def handle_starttag(self, tag, attrs):
        # print(f'start: {tag}, {attrs}')
        if ('class', 'event-title') in attrs:
            self.__flag = 'name'
        elif tag == 'time':
            self.__flag = 'time'
        elif ('class', 'say-no-more') in attrs:
            self.__flag = 'year'
        elif ('class', 'event-location') in attrs:
            self.__flag = 'location'

    def handle_endtag(self, tag):
        # print(self.data)
        if tag == 'li' and self.data:
            self.info.append(self.data)
            self.data = {}
        self.__flag = ''

    # def handle_startendtag(self, tag, attrs):
    #     print('<%s/>' % tag)

    def handle_data(self, data):
        # print('data: ',data)
        if self.__flag == 'name':
            self.data['name']  = data
        elif self.__flag == 'time':
            self._time = re.sub(r'\u2013', '-', data)
        elif self.__flag == 'year':
            if re.match(r'\s\d{4}', data):
                year = re.sub(r'\D', '', data)
                self.data['date'] = self._time + year
        elif self.__flag == 'location':
            self.data['location'] = data

    # def handle_comment(self, data):
    #     print('<!--', data, '-->')
    #
    # def handle_entityref(self, name):
    #     print('&%s;' % name)
    #
    # def handle_charref(self, name):
    #     print('&#%s;' % name)

    def to_json(self):
        d = { 'data': self.info }
        return d


parser = MyHTMLParser()
parser.feed(xml)
d = parser.to_json()
# print(d)
print(json.dumps(d, sort_keys=True, indent=4))
'''


# 正式方式解析HTML
from urllib import request
import re
Name = r'<h3 class="event-title"><a href=".*">(.*)</a></h3>'    #匹配名称的正则
Location = r'<span class="event-location">(.*)</span>'          #匹配地点的正则
Time = r'<time datetime=".*">(.*)<span class="say-no-more">'    #匹配时间的正则
Year = r'<span class="say-no-more">(.*)</span></time>'          #匹配年份
def main():
    URL = 'https://www.python.org/events/python-events/'
    data = delInf(URL)

#处理html内的信息并输出正则到的内容
def delInf(URL):
    datalist = []
    strInf = request.urlopen(URL).read().decode('utf-8')  #整个网页的信息采用utf-8的编码格式来
    name = re.findall(Name, strInf)       #正则匹配内容，返回所有匹配到的项，返回的是一个列表形式
    location = re.findall(Location, strInf)
    time = re.findall(Time, strInf)
    year = re.findall(Year, strInf)
    for index in range(0, len(name)):
        print('会议名称:'+name[index])
        print('会议地点:' + location[index])
        print('会议时间:' + time[index].replace('&ndash;','-'))  #由于特殊字符的存在，这里要替换一下
        print('会议年份:' + year[index]+'\n')

if __name__ == '__main__':
    main()
