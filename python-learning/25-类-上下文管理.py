#!/usr/bin/env python
#-*- coding: utf-8 -*-

# 类-魔术方法

# 上下文管理
    # with可以开启一个上下文运行环境，在执行前做一些准备工作，执行后做一些收尾工作。

class Query:

    def __init__(self, name):
        self.name = name
        print('1, init ~~')

    def __enter__(self):         # 该方法返回值绑定到as子句指定的变量上
        print('2, enter ~~~')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            print('3, error ~~~')   # 捕获到异常执行这里
        else:
            print('4, exit ~~~')

    def query(self):
        print('5, query ~~~', self.name)

with Query('xiaopf') as q:
    print('6, with_start ~~~')
    # raise Exception('*** error ***')
    q.query()
    print('7, with_end ~~~')

print('-'*30)

# 上下文应用场景
    # 1. 增强功能，函数执行前后，类似装饰器功能
    # 2. 资源管理，打开了资源需要关闭，如文件、网络、数据库等
    # 3. 权限验证，执行代码前做权限验证，在 __enter__ 中处理

from time import sleep
from datetime import datetime

def add(x, y):
    sleep(2)
    return x + y

class Timeit:

    def __init__(self, fn):
        self.__fn = fn

    def __enter__(self):
        self.start = datetime.now()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        timedelta = (datetime.now() - self.start).total_seconds()
        print('{} took {}s'.format(self.__fn.__name__, timedelta))

    def __call__(self, *args, **kwargs):
        self.__fn(*args, **kwargs)

with Timeit(add) as t:
    add(4, 5)
    t(4, 5)




# 使用 @contextmanager 实现
from contextlib import contextmanager

@contextmanager
def timeit(fn):
    start = datetime.now()
    yield fn      # 返回值绑定as后的变量
    timedelta = (datetime.now() - start).total_seconds()
    print('{} took {}s'.format(fn.__name__, timedelta))

with timeit(add) as t:
    add(4,5)
    t(4,5)




# 希望在某段代码执行前后自动执行特定代码:
@contextmanager
def tag(name):
    print("<%s>" % name)
    yield
    print("</%s>" % name)

with tag("h1"):
    print("hello")
    print("world")

'''
# 上述代码执行结果为：

<h1>
hello
world
</h1>
'''