#!/usr/bin/env python
# -*- coding: utf-8 -*-

# IO多路复用

# select(fds, 1024个位, 1024个写, 标志位), 使用select只能管1024路, bitmap位图
# fd: 0 1 2 3 ~ 1023
# 每一次都要遍历fds,效率低

# poll 使用数组, fds, 每一个fd结构体, 包含fd、读、写, poll突破了1024个状态
# for fd in fds:
# 判断fd对应的结构体里面读写标志是否ok
# 效率也不高

# epoll Linux Kernel 2.5+ 事件(中断)驱动, 每次只返回就绪的fds
# 排序, 重排, 导致就绪的跑到数据结构的最前面
# 提高效率, Nginx

import socket
import selectors

server = socket.socket()
server.bind(('127.0.0.1', 9999))
server.listen()
# 建议所有IO对象非阻塞
server.setblocking(False)
# newscock, raddr = server.accept()

selector = selectors.DefaultSelector()  # 自动选择最优的IO模型, IO监控只有读或者写
key = selector.register(server, selectors.EVENT_READ, 12334)  # selector 请帮我盯着server的读第一阶段就绪
print(key)  # SelectorKey, fileobj, fd, Events, data | data 标记哪个server

while True:
    events = selector.select()  # 我开始盯着注册的IO了, 盯着第一阶段，等连接过来
    print(type(events), events)  # List, fds

    for key, mask in events:
        if key.data == 12334:
            newsock, raddr = key.fileobj.accept()  # server.accept # 第二阶段
            # data = newsock.recv(1024)
            # msg = 'from {}:{}, data={}'.format(*raddr, data)
            # newsock.send(msg.encode())
            newsock.setblocking(False)
            selector.register(newsock, selectors.EVENT_READ, 2233)
        if key.data == 2233:
            data = key.fileobj.recv(1024)
            print(data, '++++')


# --------------------


# 函数模式，实现EchoServer
import socket
import selectors

server = socket.socket()
server.bind(('127.0.0.1', 9999))
server.listen()
# 建议所有IO对象非阻塞
server.setblocking(False)
# newscock, raddr = server.accept()

def accept(sock, mask):
    newsock, raddr = sock.accept()   # 什么时候做，第一阶段完成
    newsock.setblocking(False)
    selector.register(newsock, selectors.EVENT_READ, recv)

selector = selectors.DefaultSelector()
print(type(selector))   # selectors.EpollSelector 接口统一，自动选择

key = selector.register(server, selectors.EVENT_READ, accept)   # data标志位设置为一个函数
print(key)  # SelectorKey, fileobj, fd, Events, data | data 标记哪个server

def recv(sock, mask):
    data = sock.recv(1024)
    msg = "From {}.data={}".format(sock.getpeername(), data)
    sock.send(msg.encode())

while True:
    events = selector.select()     # 只把就绪返回，返回就绪列表
    print(type(events), events)
    for key, mask in events:
        key.data(key.fileobj, mask)
        # if key.data == accept:
        #     key.data(key.fileobj, mask)
        # if key.data == recv:
        #     key.data(key.fileobj, mask)


# --------------------


# 用IO多路复用改写ChatServer
import socket
import selectors
import threading


class ChartServer:
    def __init__(self, ip='127.0.0.1', port=9999):
        self.addr = ip, port
        self.server = socket.socket()
        self.server.setblocking(False)  # 非阻塞
        self.selector = selectors.DefaultSelector()  # 最优
        self.event = threading.Event()

    def start(self):
        self.server.bind(self.addr)
        self.server.listen()

        key = self.selector.register(self.server, selectors.EVENT_READ, self.accept)
        threading.Thread(target=self.select, name='select').start()

    def select(self):
        with self.selector:
            while not self.event.is_set():
                events = self.selector.select(0.5)  # 阻塞0.5s
                for key, mask in events:
                    key.data(key.fileobj, mask)

    def accept(self, server: socket.socket, mask):
        conn, raddr = server.accept()
        conn.setblocking(False)

        key = self.selector.register(conn, selectors.EVENT_READ, self.recv)

    def recv(self, conn: socket.socket, mask):
        data = conn.recv(1024).strip()
        if data == b'' or data == b'quit':
            # 客户端主动断开需要取消注册，注销在关闭之前
            self.selector.unregister(conn)
            conn.close()
            return
        msg = "From {}.data={}".format(conn.getpeername, data)
        # conn.send(msg.encode())
        for key in self.selector.get_map().values():
            if key.data == self.recv:  # is ==
                key.fileobj.send(msg.encode())

    def stop(self):
        self.event.set()
        # self.selector.close()


if __name__ == '__main__':
    cs = ChartServer()
    cs.start()
    while True:
        cmd = input('>>').strip()
        if cmd == 'quit':
            cs.stop()
            break
        print(*cs.selector.get_map().items())  # (fd, key)





# 用IO多路复用实现 WWW Server

import socket
import selectors
import threading
import webob

test_html_content = """
<html>
<head>
<title>测试网页</title>
<body>
欢迎访问
</body>
</head>
</html>
"""


class WWWServer:
    def __init__(self, ip='localhost', port=80):
        self.addr = ip, port
        self.server = socket.socket()
        self.server.setblocking(False)  # 非阻塞
        self.selector = selectors.DefaultSelector()  # 最优
        self.event = threading.Event()

    def start(self):
        self.server.bind(self.addr)
        self.server.listen()

        key = self.selector.register(self.server, selectors.EVENT_READ, self.accept)
        threading.Thread(target=self.select, name='select').start()

    def select(self):
        with self.selector:
            while not self.event.is_set():
                events = self.selector.select(0.5)  # 阻塞0.5s
                for key, mask in events:
                    key.data(key.fileobj, mask)

    def accept(self, server: socket.socket, mask):
        conn, raddr = server.accept()
        conn.setblocking(False)
        key = self.selector.register(conn, selectors.EVENT_READ, self.recv)

    def recv(self, conn: socket.socket, mask):
        try:
            data = conn.recv(1024)
            # print(data)
            request = webob.Request.from_bytes(data)
            # print(request.url)  # 不同的url返回不同的结果，URL映射
            # print(request.path)
            response = webob.Response(test_html_content)
            firstline = 'HTTP/1.1 {}'.format(response.status)
            response.headers.add('Server', 'MyServer')   #  自定义添加Header头
            header = "\r\n".join(
                [firstline] +
                ["{}: {}".format(k, v) for k, v in response.headerlist] +
                ['', '']
            ).encode()
            conn.send(header + response.body)  # 响应header和body体
        finally:
            self.selector.unregister(conn)
            conn.close()

    def stop(self):
        self.event.set()
        # self.selector.close()


if __name__ == '__main__':
    cs = WWWServer('0.0.0.0')
    cs.start()

# URL
# http://www.xxx.com/path/path1
# HTTP request 格式：数据 bytes str 每一行换行必须是\r\n
# HTTP reqeust 报文 2部分
    # 1 header: firstline + \r\n + 其他行 \r\n\r\n
    # 2 body 可以没有

# HTTP response
    # 1 header: firstline + \r\n + 其他行 \r\n\r\n
        # xxx: yyy
    # 2. body: 正文，字符串

# 连接：连一下，一次请求响应，断开