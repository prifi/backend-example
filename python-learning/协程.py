#!usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: fly
@time: 2022/07/04
@file: 协程.py
@describe:  
"""
# 异步IO
"""
协程 coroutine：
    协程是通过程序自身的控制（生成器特性），去切换不同任务，实现单一线程并发的效果。
    执行效率高，没有线程切换开销
    没有多线程的锁机制，因为只有一个线程
    利用多核CPU，使用多进程+协程

"""


# Python对协程的支持是通过generator实现的，yield可以接收调用者发出的参数，生产消费使用协程，效率高
def consumer():
    r = ''
    while True:
        n = yield r  # 赋值语句先计算= 右边，由于右边是 yield 语句，所以yield语句执行完以后，进入暂停，而赋值语句在下一次启动生成器的时候首先被执行
        if not n:
            return
        print('[CONSUMER] Consuming %s...' % n)
        r = '200 OK'


def produce(c):
    c.send(None)  # Python的yield不但可以返回一个值，它还可以接收调用者发出的参数。
    n = 0
    while n < 5:
        n = n + 1
        print('[PRODUCER] Producing %s...' % n)
        r = c.send(n)
        print('[PRODUCER] Consumer return: %s' % r)
    c.close()


c = consumer()
produce(c)



# 用asyncio的异步网络连接来获取sina、sohu和163的网站首页
import asyncio
import threading

# async定义一个协程，await用于挂起阻塞的异步调用接口。
async def wget(host):
    print('wget {}...'.format(host))
    connect = asyncio.open_connection(host, 80)
    reader, writer = await connect
    header = 'GET / HTTP1.1\r\nHOST: {}\r\n\r\n'.format(host)
    writer.write(header.encode('utf-8'))
    await writer.drain()
    while True:
        line = await reader.readline()
        if line == b'\r\n':
            break
        print('{} header > {}'.format(host, line.decode('utf8').rstrip()))
    writer.close()

loop = asyncio.get_event_loop()
tasks = [wget(host) for host in ['www.sina.com.cn', 'www.sohu.com', 'www.163.com']]
loop.run_until_complete(asyncio.wait(tasks))
loop.close()