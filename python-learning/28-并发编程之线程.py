#!/usr/bin/env python
#-*- coding: utf-8 -*-

# 并发编程


# Thread类
    # def __init__(self, group=None, target=None, name=None, args=(), kwargs=None, *, daemon=None)
    # 启动一个线程就是把一个函数传入并创建Thread实例，然后调用start()开始执行

import threading
import time

def worker(name, age):
    # time.sleep(20)
    print('working~~~~~')
    # while True:     # 死循环
    for i in range(10):
        time.sleep(1)
        if i > 5:
            # break   # 终止循环，正常执行
            # return  # 函数返回，看不到finished
            1/0       # 抛出异常，工作线程崩溃意外退出，exit_code为0
        print('='*30)
    print('finished~~~~~')

t = threading.Thread(target=worker, name='worker', args=('xiaopf',), kwargs={'age': 8})    # 只是创建了一个线程管理对象
t.start()   # 调用 系统调用，创建真正的操作系统线程，启动运行target函数
# 2 / 0     # 进程exit_code为非0


# 线程退出
    # 1,线程函数正常执行完
    # 2,线程函数中抛出未处理的异常，退出状态码为0


# Threading属性及方法：
'''
    t.name    线程名，可重名
    t.ident   线程ID
    t.is_alive()   线程是否存活
    threading.main_thread()     返回主线程对象
    threading.current_thread()  返回当前线程对象
    threading.active_count()    当前处于alive状态线程个数
    threading.current_thread().ident
    threading.enumerate()       活着的线程列表
'''


# start 和 run 的本质
    # 可以简化调用，重写run方法

def worker():
    print('working~~~~~')
    for i in range(10):
        time.sleep(0.5)
        print('='*15, i, '='*15)
    print('finished~~~~~')

class MyThread(threading.Thread):
    def __init__(self, name):
        super().__init__()
        self._name = name

    def start(self) -> None:  # 创建操作系统线程，把未来要执行的目标函数送进去
        print('start~~~~~')
        super().start()

    def run(self) -> None:
        print('run~~~~~', self._name)     # 执行目标函数
        super().run()

t = MyThread(target=worker, name='worker')
t.start()


# Thread实例的属性和方法
x = threading.main_thread()
print(x.name, x.ident, x.is_alive())

while True:
    time.sleep(1)
    if t.is_alive():
        print(threading.active_count(), threading.enumerate())
    if threading.active_count() == 1:
        print('I will restart t')
        t.start()    # 异常：RuntimeError: threads can only be started once


# daemon
    # daemon=True,   daemon=False non-daemon
    # daemon手动设置True/False，如果不设置，默认None取当前线程的demon值（继承主线程）
    # 没有活着的non-daemon程序退出，还有daemon线程，主线程退出则直接kill掉

t1 = threading.Thread(target=worker, name='worker1', args=('t1', 5, '#') ,daemon=False)
t1.setDaemon(threading.current_thread().daemon)    # 设置daemon值，继承当前线程的daemon值，daemon一定要在start之前设置
t1.start()
t1.join(2)   # 阻塞，join谁等谁, join t1, 主线程阻塞等t1
print('~'*30)
t1.join()    # 不写时间一直等
print('='*30)
# daemon=True,   daemon=False non-daemon
print(threading.enumerate())    # False, 主线程是non-daemon线程


# join
    # 一个线程调用另一个线程的join方法，调用者将被阻塞直到被调用者停止
    # join需要在start之后
    # 阻塞，join谁等谁, join t1, 主线程阻塞等t1

import time
from threading import Thread

def work():
    for i in range(10):
        time.sleep(1)
        print('work ~~~')

t = Thread(target=work, daemon=True)
t.start()
t.join(5)  # 5s后全部线程退出，如果是non-daemon则等待

print('main ----')



# daemon线程应用场景：
    # 1.后台任务，心跳包、监控场景
    # 2.主工作线程一起退出，减少手动关闭工作量，快速关闭方法
    # 3.随时被终止



# threading.local 类
    # 为每一个线程创建不同的local值，使每个线程互不干扰
    # 解决在单一线程中，多个函数之间传递值

import threading
import time
import logging

FORMAT = "%(asctime)s %(threadName)s %(thread)s %(message)s"
logging.basicConfig(format=FORMAT, level=logging.INFO)

class A():
    def __init__(self):
        self.x = 0

x = 0
global_data = A()
global_local = threading.local()

def worker():
    logging.info('working~~~~~')
    # x = 0               # x 是局部变量，局部变量和每一次函数调用的栈帧有关
    # 如果多线程运行，使用的都是局部变量，那很安全
    # global x            # 使用全局变量，线程不安全
    # global_data.x = 0   # 使用全局对象，线程也不安全，线程之间互相干扰
    global_local.x = 0    # 安全，互不干扰，结果与使用局部变量一样
    for i in range(1000):
        time.sleep(0.00001)
        # x += 1
        # global_data.x +=1
        global_local.x += 1
    logging.info(f'finished~~~~~ {threading.current_thread().name} => {global_local.x}')

for i in range(10):
    threading.Thread(target=worker, name=f't-{i}').start()

'''
threading.local本质：
    属性不能跨线程，构建了一个大字典存放所有线程相关的字典（大字典套小字典）=> { id(Thread) -> (ref(thread), thread-local dict) }
                                                                        线程实例id      线程对象引用      线程自己字典
    运行时，threading.local实例处在不同的线程中，从大字典中找到当前线程相关键值对中的字典，覆盖threading.local实例的__dict__。
    这样就可以在不同的线程中安全地使用线程独有的数据，做到了线程间数据隔离，如同本地变量一样安全
'''


# 使用类方法的多线程

import time
from threading import Thread

class Work:
    def __init__(self, x):
        self.x = x

    def worker(self, n):
        for _ in range(n):
            time.sleep(1)
            self.x += 1
            print('worder ~~~ {}'.format(self.x))


class MyThread(Thread):
    def __init__(self, a):
        super().__init__(daemon=True)
        self.a = a

    def run(self) -> None:
        Work(self.a).worker(10)
        # for _ in range(5):
        #     time.sleep(1)
        #     print(f'{self.__class__.name} ~~~ {a}')

class MyThread2(Thread):
    def __init__(self, a):
        super().__init__(daemon=True)
        self.a = a

    def run(self) -> None:
        Work(self.a).worker(5)
        # for _ in range(5):
        #     time.sleep(1)
        #     print(f'{self.__class__.name} ~~~ {a}')

t = MyThread(0)
t1 = MyThread2(0)
t.start()
t1.start()
t.join()
t1.join()
print('='*30)