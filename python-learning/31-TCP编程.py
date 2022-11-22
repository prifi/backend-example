#!/usr/bin/env python
# -*- coding: utf-8 -*-


# 三层路由，四层进程
# TCP数据流，UDP数据报文

# Server
    # Socket - bind(IP, PORT) - listen - accept - close
    #                                       |- recv or send - close


# 基本用法   服务端
import sys
import socket

# 建立TCP Socket
server = socket.socket()

# addr 必须是元组
addr = '0.0.0.0', 9999
server.bind(addr)

# 监听端口
server.listen()     # 半连接队列，队列有大小
print(server, file=sys.stderr)
    # <socket.socket fd=3, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, proto=0, laddr=('127.0.0.1', 9999)>

# x = server.accept()   # 阻塞方法
# print(type(x), x)
    # <class 'tuple'> (<socket.socket fd=4, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, proto=0, \
    # laddr=('127.0.0.1', 9999), raddr=('127.0.0.1', 33810)>, ('127.0.0.1', 33810))

# 阻塞等待连接
newsock, raddr = server.accept()
print(newsock.getpeername())   # 客户端     ('127.0.0.1', 33812)
print(newsock.getsockname())   # 本地服务端  ('127.0.0.1', 9999)

# 发送数据，无连接UDP协议使用 sedto，协议+地址+端口
newsock.send(b'abcdef\n')

# 接收数据，缓冲区大小 2的幂数
data = newsock.recv(1024)     # 也是一个阻塞方法，等待接收数据
print(type(data), data)
msg = "data = {}".format(data.strip())
print(msg)
newsock.send(msg.encode())

server.close()




# 实现一个群聊工具server端
    # 1.EchoServer 回声
    # 2.线程安全，加锁
import logging
import socket
import threading

class ChatServer:
    def __init__(self, ip='127.0.0.1', port=9999):
        self.addr = ip, port
        self.sock = socket.socket()
        self.event = threading.Event()   # 停止socker事件
        self.clients = {}                # 群发记录socket
        self.lock = threading.Lock()     # 线程安全

    def start(self):
        self.sock.bind(self.addr)
        self.sock.listen()
        # 为了不阻塞主线程
        threading.Thread(target=self.accept, name='accept').start()

    def accept(self):   # 多人连接
        count = 1
        while not self.event.is_set():
            # 为每个连接单独创建线程
            newsock, raddr = self.sock.accept()
            with self.lock:
                self.clients[raddr] = newsock    # 添加客户端字典
            # 扔给多线程函数处理，避免阻塞
            threading.Thread(target=self.recv, name=f'r-{count}', args=(newsock, raddr)).start()
            count += 1

    def recv(self, sock:socket.socket, raddr):
        while not self.event.is_set():
            try:
                data = sock.recv(1024).strip()
            except Exception as e:     # 非正常退出
                logging.error(e)
                data = b''
            if data == b'' or data == b'quit':
                with self.lock:
                    self.clients.pop(raddr)
                    sock.close()
                break
            msg = "from {}:{}, data={}\n".format(*raddr, data.decode())
            # 线程安全，因为字典在遍历时不能修改size
            with self.lock:
                for s in self.clients.values():
                    s.send(msg.encode())

    def stop(self):
        self.event.set()
        with self.lock:
            for s in self.clients.values():
                s.close()
        self.sock.close()


if __name__ == '__main__':
    cs = ChatServer()
    cs.start()
    print('='*30)
    while True:
        try:
            cmd = input('>>>').strip()
            if cmd == 'quit':
                cs.stop()
                break
        except KeyboardInterrupt:
            cs.stop()
            break
        print(threading.enumerate())
        print(cs.clients)



# MakeFile
    # 创建一个套接字相关连的文件对象，将recv看做读方法，将send看做写方法
import socket
server = socket.socket()
addr = '127.0.0.1', 9999
server.bind(addr)
server.listen()

newsock, raddr = server.accept()
print('-'*30)

f = newsock.makefile('rw')    # 返回文件对象
# x = f.read(5)
x = f.readline().strip()      # 按行读取
print('~'*30)
print(type(x), x)             # <class 'str'> hello 注意是文本类型

msg = "from {}:{}, data={}".format(*raddr, x)
f.write(msg)

newsock.close()
f.close()
server.close()




# 客户端编程 TCP
    # 基本用法
# client = socket.socket()
# raddr = '127.0.0.1', 9999
# client.connect(raddr)
# print(client.getpeername())  # 对端地址
# x = client.send(b'hello')    # 返回发送成功字节数
# data = client.recv(1024)     # 收到字节，阻塞等待
# client.close()

    # 客户端类
import threading

class CharClient:
    def __init__(self, rip='127.0.0.1', rport=9999):
        self.sock = socket.socket()
        self.raddr = rip, rport
        self.event = threading.Event()

    def start(self):
        try: # 做一个3次尝试启动
            self.sock.connect(self.raddr)
            self.send('hello')
        except Exception as e:
            logging.error(e)
            raise
        # 准备接收数据，recv是阻塞的，开启新线程
        threading.Thread(target=self.recv, name='recv').start()

    def recv(self):
        while not self.event.is_set():
            try:
                data = self.sock.recv(1024)
            except Exception as e:
                logging.error(e)
                break

            msg = "from {}:{}, data={}".format(*self.raddr, data)
            print(msg)

    def send(self, msg:str):
        data = "{}\n".format(msg.strip()).encode()
        self.sock.send(data)

    def stop(self):
        self.sock.close()
        self.event.wait(3)
        self.event.set()
        print('Client stops.')

def main():
    cc = CharClient()
    cc.start()
    while True:
        cmd = input('>>>')
        if cmd.strip() == 'quit':
            cc.stop()
            break
        cc.send(cmd)   # 发送消息


if __name__ == '__main__':
    main()




# SocketServer
    # 对底层sokcet进行封装的网络服务编程框架

import socketserver

class MyHandler(socketserver.BaseRequestHandler):
    def handle(self) -> None:
        print('='*30)
        print(self.request)          # 客户端连接的socket对象，与客户端通信
        print(self.client_address)   # 客户端IP地址+端口
        print(id(self.server), self.server)     # TCPServer实例本身
        for i in range(3):
            data = self.request.recv(1024)
            msg = 'from {}:{},data={}'.format(*self.client_address, data)
            self.request.send(msg.encode())
        print('='*30)

server = socketserver.TCPServer(('127.0.0.1', 9999), MyHandler)  # => BaseRequestHandler(request, class_address, server)
print(id(server))
server.handle_request()   # 处理一次请求，阻塞方法

'''
140071948595152
==============================
<socket.socket fd=4, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, proto=0, laddr=('127.0.0.1', 9999), raddr=('127.0.0.1', 33272)>
('127.0.0.1', 33272)
140071948595152 <socketserver.TCPServer object at 0x7f650abd2fd0>
==============================
'''


# 多线程，与多个客户端进行通信，改造群聊服务ChartServer
    # 线程安全？ --有，需要加锁，跨多线程使用同一把锁(类属性)
import threading
import socketserver
class CharHandler(socketserver.StreamRequestHandler):
    clints = {}

    def setup(self) -> None:
        super().setup()
        self.event = threading.Event()
        self.clints[self.client_address]  = self.wfile

    def handle(self) -> None:
        super().handle()
        while not self.event.is_set():
            try:
                data = self.rfile.readline().strip()   # bytes
            except Exception as e:
                logging.error(e)
                data = b''
            if data == b'' or data == b'quit':
                break
            msg = 'from {}:{},data={}'.format(*self.client_address, data)
            for c in self.clints.values():
                c.write(msg.encode())
                c.flush()

    def finish(self) -> None:
        self.clints.pop(self.client_address)
        super().finish()
        self.event.set()


class ChartServer:
    def __init__(self, ip='127.0.0.1', port=9999, HandlerClass=CharHandler):
        self.addr = ip, port
        self.server = socketserver.ThreadingTCPServer(self.addr, HandlerClass)

    def start(self):
        self.server.serve_forever()

    def stop(self):
        self.server.server_close()


if __name__ == '__main__':
    cs = ChartServer()
    cs.start()