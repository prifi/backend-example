#!usr/bin/env python
# -*- coding:utf-8 _*-
"""
@version:
author:xiaopengfei
@time: 2021/02/03
@file: 04_1-高阶函数map+reduce+filter.py
@function:
@modify:
"""

# 1.map
# map()函数接收两个参数，一个是函数，一个是Iterable，map将传入的函数依次作用到序列的每个元素，并把结果作为新的Iterator（迭代器）返回。
def f(x):
    return x * x

r = map(f,[1,2,3,4,5,6,7])  # 返回 [ 1*1, 2*2, 3*3, ... ]
print(type(r))   # <class 'map'>  惰性序列，map对象
print(list(r))   # [1, 4, 9, 16, 25, 36, 49]

# list所有数字转为字符串
slst = list(map(str, [1,2,3,4,5]))
print(slst)  # ['1', '2', '3', '4', '5']



## 2.reduce
# reduce把一个函数作用在一个序列[x1, x2, x3, ...]上，这个函数必须接收两个参数，reduce把结果继续和序列的下一个元素做累积计算
# reduce(f, [x1, x2, x3, x4]) = f(f(f(x1, x2), x3), x4)
from functools import reduce
def add(x, y):
    return x + y
num = reduce(add, [1,2,3,4,5])
print(type(num))  # <class 'int'> 整数

def fn(x, y):
    return x * 10 + y
print(reduce(fn, [1,2,3,4,5]))   # 12345

# 配合map()，可以写出把str转换为int的函数
from functools import reduce
DIGITS = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9}
def str2int(s):
    def fn(x, y):
        return x * 10 + y
    def char2num(s):
        return DIGITS[s]
    return reduce(fn, map(char2num, s))

print(str2int('13579'))  # 13579

# 求列表乘积
def prod(L):
    return reduce(lambda x, y: x * y, L)
print('3 * 5 * 7 * 9 =', prod([3, 5, 7, 9]))

# 练习：利用map和reduce编写一个str2float函数，把字符串'123.456'转换成浮点数123.456
# 解法1：
# from functools import reduce
# def str2float(s):
#     slt = s.split('.',1)
#     def char2num(s):
#         DIGITS = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9}
#         return DIGITS[s]
#     def fn(x,y):
#         return x * 10 + y
#     def fun(a, b):
#         i = reduce(fn, map(char2num, a))
#         f = reduce(fn, map(char2num, b))
#         return i + f / 10 ** len(b)
#     return fun(slt[0],slt[1])
#
# fl = str2float('123.456')
# print(fl)

# 解法2：
from functools import reduce
def str2flot(s):
    a,b  = s.split('.', 1)
    s1 = a + b
    def char2num(s):
        DIGITS = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9}
        return DIGITS[s]
    return reduce(lambda x,y:x * 10 + y, map(char2num, s1)) / (10 ** len(b))
print(str2flot('123.456'))

# 解法3：b[::-1] 反转字符串，'abc' => 'cba'
from functools import reduce
def str2flot(s):
    a,b = s.split('.', 1)
    return reduce(lambda x, y: x * 10 + y, map(int, a)) + reduce(lambda x, y: x * 0.1 + y, map(int, b[::-1]))/10
print(str2flot('123.456'))



## 3.filter
# filter()函数用于过滤序列，接收一个函数和序列，根据返回值是True还是False决定保留还是丢弃该元素。
# filter()函数返回的是一个Iterator，也就是一个惰性序列，需要用list()获取所有结果并返回list

## 求奇数
def is_add(n):
    return n % 2 == 1
print(list(filter(is_add, list(range(15)))))
# 结果：[1, 3, 5, 7, 9, 11, 13]
# 等同于：[x for x in list(range(15)) if x % 2 == 1 ]

## 删除序列中的空字符串
def is_empty(s):
    return s and s.strip()
print(list(filter(is_empty, ['aaa', ' ', 'bbb'])))

## 求素数
def _odd_iter():
    # 构造3开始的惰性序列：3,5,7 ..
    n = 1
    while True:
        n += 2
        yield n
def _not_divisble(n):
    # 定义筛选函数
    return lambda x: x % n > 0
def primes():
    # 利用filter()不断产生筛选后新的序列
    yield 2
    it = _odd_iter()
    while True:
        n = next(it)
        yield n
        it = filter(_not_divisble(n), it)
# primes()也是一个无限序列，退出循环条件
for n in primes():
    if n < 100:
        print(n, end=' ')
    else:
        break
# 结果：2 3 5 7 11 13 17 19 23 29 31 37 41 43 47 53 59 61 67 71 73 79 83 89 97


## 练习：利用filter()筛选出回数，例如12321，909
def is_palindrome(n):
    return str(n)[0:-1:] == str(n)[-1:0:-1]
# list(filter(is_palindrome, list(range(152))))



## 4.sorted
# 排序算法，对list进行排序
# 字符串排序按ascii码排序
sorted([36, 5, -12, 9, -21])
sorted([36, 5, -12, 9, -21], key=abs)
sorted([1,2,3,4,-5], key=abs, reverse=True)  # 倒序

# 练习：用sorted()对上述列表分别按名字排序
L = [('Bob', 75), ('Adam', 92), ('Bart', 66), ('Lisa', 88)]
def by_name(t):
    return t[0]
# sorted(L, key=by_name)

# 练习：按分数从高到低排序
def by_sorce(t):
    # - 倒序
    return -t[1]
# sorted(L, key=by_sorce)







