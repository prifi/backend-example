#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 函数参数、解构、返回值、作用域

# 函数

## 位置&缺省参数

# * 定义时，位置参数在前，关键字（缺省）参数在后
# def add(x=3, y):   # 错误写法
#     return x + y


## 位置参数在前，缺省值，复杂的，*args靠后，**kwargs最后
def fn(x, y=5, *args, **kwargs):
    print(x, y, args, kwargs)
fn(1, b=2, a=5, y=3)  # 正确
# fn(x=4, y=3, 1, 2, a=1, b=2)  # 错误，实参传入时，位置传参在前，关键字在后
fn(1, 2, x=1, a='abc')  # 错误，重复传参 x


## keyword-only 参数, *, *args
def foo(*, x, y):
    print(x, y)
foo(x=2, y=1)


## Positional-only 参数，仅位置参数
def add(a, b, /):
    print(a, b)
add(1, 2)

# sorted(iterable, /, *, key=None, rervese=False)



## 参数混合示例
def fn(a, b, /, x, y, z=3, *args, m=4, n, **kwargs):
    pass

# 实参变动小的在后
def connect(host='localhost', user='admin', password='admin', port='3306', **kwargs):
    print('mysql://{}:{}@{}:{}/{}'.format(
        user, password, host, port, kwargs.get('db', 'test')
    ))
connect()
connect(db='cmdb')



## 参数解构
def add(x, y):
    print(x, y)
    return x + y
# 以下都可以传参
add(*(4,5)), add(*{4,5}), add(*{'a':1, 'b':2}), add(**{'x':100, 'y':110})
# * -> 位置参数
# ** -> 关键字传参


## 返回值
def values():
    return 1,3,5,7
x, *_, z = values()  # 返回tuple,使用解构的思想接收


## 三元表达式返回
def guess(x):
    return f'{x}' if x > 3 else -1

nums = [1, 3, 5, 7, 9]
print(id(nums))
gen = (n for n in nums if n in nums)
nums = [1, 2, 3, 4]
print(id(nums))
print(list(gen))



## 变量作用域
# 向内穿透、对外不可见、优先自己

## global 尽量少用，变量污染
x = 5
def foo():
    # global x
    # x += 1      # 被判定为局部变量，x= 为赋值
                # x = x + 1 UnboundLocalError: local variable 'x' referenced before assignment
    print(x)
foo()

# global 尽量少用，使用传实参的形式
z = 123
def fn1(z):
    z +=1
    print(z)
fn1(z)