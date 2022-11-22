#!usr/bin/env python
# -*- coding:utf-8 -*-
'''
# 官方文档：https://docs.python.org/zh-cn/3/howto/urllib2.html
# urllib.request 获取页面
urllib.request.urlopen(url, data=None, [timeout,]*,
                      cafile=None, capath=None,
                      cadefault=False, context=None)
'''


from urllib import request, parse, error


# GET
def get_method():
    with request.urlopen('http://www.baidu.com') as f:
        data = f.read()
        print('Status', f.status, f.reason)
        for k,v in f.getheaders():
            print(f'{k}:{v}')
        print('Data', data.decode('utf-8'))


# GET + Headers
def get_method_header():
    # 1.字典方式
    headers = {'User-Agent': 'Mozilla/6.0'}
    req = Request(url='http://www.baidu.com', headers=headers)

    # 2.add_header添加
    req = Request(url='http://www.baidu.com')
    req.add_header('User-Agent', 'Mozilla/6.0')

    with request.urlopen(req) as f:
        try:
            data = f.read().decode()
        except URLError as e:
            if hasattr(e, 'reason'):
                raise ('Reason: ', e.reason)
            elif hasattr(e, 'code'):
                raise('Error code: ', e.code)
        else:
            # dp = json.loads(data)
            pass

'''
# 方法
response.read().decode()
response.readlines()
response.geturl()
response.getcode()
response.status
response.reason
response.getheaders()
response.getheader('Content-Type')
'''


# POST
def post_method():
    url = 'http://httpbin.org/post'
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64)',
        'Host':'httpbin.org'
    }

    # 以username=xxx&password=xxx编码传入
    # login_data = parse.urlencode([
    #     ('username', 'email'),
    #     ('password', 'passwd'),
    # ])
    # data = login_data.encode('utf-8')   # 传入到Request对象中

    data = {'name': "Germey"}
    data = parse.urlencode(data).encode('utf-8')
    req = request.Request(url=url, headers=headers, data=data, method='POST')
    with request.urlopen(req) as response:
        page = response.read().decode()
    # response = request.urlopen(req)


# 异常处理
'''
URLError
    - HTTPError
        - code: 404, 429, 500 ...
        - reason: 异常原因
        - headers: 请求头
        
except HTTPError 必须 首先处理，否则 except URLError 将会 同时 捕获 HTTPError
'''
from urllib.request import Request, urlopen
from urllib.error import URLError

def herror():
    someurl = 'http://www.sunfloweer.com'
    req = Request(someurl)
    try:
        response = urlopen(req)
    except URLError as e:
        if hasattr(e, 'reason'):
            print('We failed to reach a server.')
            print('Reason: ', e.reason)
        elif hasattr(e, 'code'):
            print('The server couldn\'t fulfill the request.')
            print('Error code: ', e.code)
    else:
        # everything is fine
        print('Successfully!')


# 超时异常处理
import socket
def tot():
    try:
        response = request.urlopen('http://www.baidu.com', timeout=0.001)
    except error.URLError as e:
        print(type(e.reason))
        if isinstance(e.reason, socket.timeout):
            print('TIME OUT')


# 添加Cookie
from http import cookies


# Hander 代理
from urllib.request import ProxyHandler, ProxyBasicAuthHandler, build_opener
def hd():
    proxy_handler = ProxyHandler({'http': 'http://www.example.com:3128/'})
    proxy_auth_handler = ProxyBasicAuthHandler()
    proxy_auth_handler.add_password('realm', 'host', 'username', 'password')
    opener = build_opener(proxy_handler, proxy_auth_handler)
    with opener.open('http://www.example.com/login.html') as f:
        pass