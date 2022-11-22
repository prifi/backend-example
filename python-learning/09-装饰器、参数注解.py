#!/usr/bin/env python
#-*- coding: utf-8 -*-

# 高阶函数，装饰器

    # iter   -> 注意迭代指针，不可回头
    # next
    # reversed
    # enumerate
    # sorted  -> 返回list, key=?
    # filter  -> 真留
    # map  ->  dict(map(lambda *args: (str(args[0]),args[1]), range(10),range(10)))
    # zip

# 高阶函数定义：
    # 函数参数、返回值是函数时


# 柯里化  f(x,y) => f(x)(y)

def add(x, y):
    return x + y

def add(x):
    def inc(y):
        return x + y
    return inc
add(4)(5)



# time 模块
# 获取运行时间
import time
import datetime
def time_demo():
    start = datetime.datetime.now()
    time.sleep(5)
    end = datetime.datetime.now()
    return (end - start).total_seconds()



# 装饰器
# def add(x, y):
#     return x + y

# 更新函数名字
from functools import update_wrapper, wraps

# 记录函数运行时间
def logger(wrapped):
    @wraps(wrapped)  # 使用 wrappend 替换 wrapper， wrapper = wraps(wrapped)(wrapper)
    def wrapper(*args, **kwargs):
        # 函数执行前操作
        start = datetime.datetime.now()
        ret = wrapped(*args, **kwargs)
        # 函数执行后操作
        delta = (datetime.datetime.now() - start).total_seconds()
        print("{} tooks {}s".format(wrapped.__name__, delta))
        return ret
    # wraps 装饰器版本
    # update_wrapper(wrapper, wrapped)
    return wrapper

# add = logger(add)
# add(4, y=5)

@logger   # 等价式， add = logger(add)  # logger 应该等效为单参函数
def add(x, y):
    "add description"
    time.sleep(0.1)
    return x + y

# add(4, y=8)
# print(add.__name__)  # 名字还是返回的 wrapper
# print(add.__doc__)


"""
# 两种带参数装饰器伪代码

# 参数在后
def require_http_methods(['GET', 'POST']):
    def decorator(func):
        def inner(request, *args, **kwargs):
                pass
            return func(request, *args, **kwargs)
        return inner
    return decorator

# 柯里化
func = require_http_methods(['GET', 'POST'])(func)(*args, **kwargs)

@require_http_methods(['GET', 'POST'])
def func(request):
    pass


# 参数在前
def log('text'):
    def decorator(func):
        def wrapper(*args, **kwargs):
            print(text)
            return func(*args, **kwargs)
        return wrapper
    return decorator

func = log(text)(func)(*args, **kwargs)
"""



# 参数注解, 3.6以上

def add(x:int, /, y, m=100, *args, **kwargs) -> list:
    '''
    参数注解
    :param x: int
    :param y: int
    :return: list
    '''
    return x + y   # 返回一个 list, 不强制要求

# a = add(4,5)
# print(add.__annotations__)


# import inspect
# inspect.isfunction(add)  # 是否是函数、类、方法、可迭代对象、内建函数 ...
#
# params = inspect.signature(add).parameters # 签名对象  返回 OrderedDict 字典记录了录入顺序
# print(params)
# print(params.values())
# print(isinstance(1, params.get('x').annotation))   # 判定参数类型
# for k,v in params.items():
#     print(v.name, v.default, v.annotation, v.kind)   # 四种属性



# 应用：参数类型检查(int)，返回值类型检查(list)
from functools import wraps
import inspect

def check(func):
    @wraps(func)
    def wrapper(*args, **kwargs):

        # 获取参数属性
        sig = inspect.signature(add)
        params = sig.parameters
        print(params)       # Parameter类，四个属性， name, default, annotation, kind

        # 位置参数类型检查
        for k, v in zip(args, params.values()):
            # 有类型注解的参数检查 v.empty
            if v.annotation is not v.empty and not isinstance(k, v.annotation):
                print('Args {} is not {} ok!'.format(k, v.annotation))
                # raise ValueError('Args {} is not {} ok!'.format(k, v.annotation))

        # 可变参数类型检查
        for k, v in kwargs.items():
            if params.get(k).annotation is not inspect._empty and not isinstance(v, params.get(k).annotation):
                print('Kwargs {} is not {} ok!'.format(v, params.get(k).annotation))

        ret = func(*args, **kwargs)

        # 返回值检查
        if sig.return_annotation is not inspect._empty and not isinstance(ret, sig.return_annotation):
            print('Return {} is not {} ok!'.format(ret, sig.return_annotation))

        return ret
    return wrapper

@check  # 等价式：add = check(add)
# def add(x:int, y:int) -> list:
def add(x, y:int) -> list:        # 假设 x 没有添加注解, 不检查 v.empty
    # print()
    return [x, y]
    # return x + y

## 验证结果
add('4','5')
# add(4,'5')
# add(4, y='5')
# add('4', y='5')
# add(y='4', x='5')
# add(4,5)