#!/usr/bin/env python
#-*- coding: utf-8 -*-

# 参数解构，字典，生成器


# 参数解构

# a, b = [1,2] | (1,2) | {1,2} | 'a', 'b'  # 个数匹配

## * 具有剩余能力
import sys

a, *r, b = range(10)
print(a,r,b)

print(sys.path)

## 分割路径， _ 代表丢弃变量
p1 = r'/data/github/devops/python/magedu'
dirname, _, basename = p1.rpartition(r'/')
print(dirname, basename)



# Dict

## 构造器
# 二元结构
# dict(()), dict([]), dict({}), dict('a'=1,)

d = dict.fromkeys('abc',[1])
d['a'][0] = 100   # {'a': [100], 'b': [100], 'c': [100]}

## 获取元素
# d[key], -> KeyError
# d.get(key, None or default)
# d.setdefault(key, None or default)

## 更新
# 就地 与构造器一致，存在则修改，无则增加
# d.update([('a',123),('b', 456)], c=True)  # None

## 遍历
# 只跟规模相关 O(n)
d = {'a':[1,2], 'b':(1,), 'c':{1,2,3}}
for k, (v,*_) in d.items():
    print(k,v)

for k in d:
    d[k] = 100
print(d)

# 遍历时不允许修改 dict,set 的size
# for 循环正确删除，分两步走
d1 = dict(a=100, b=200, c=300)
keys = []
for k, v in d1.items():
    if v > 100:
        keys.append(k)
for k in keys:
    d1.pop(k)
print(d1)



## 生成器
x = (i for i in range(10))   # 生成器表达式


## 排序 sorted
print(sorted(range(10), reverse=True))
print(sorted({'a':100, 'b':'abc'}.items()))
print(sorted({'a':100, 'b':'abc'}.values(), key=str))


# 作业

## 1.三数比大小，升序
a, b, c = 1, 5, 3
if a > b:
    a, b = b, a

if a > c:
    a, c = c, a

if b > c:
    b, c = c, b

print(a, b, c)


## 2.新列表是lst相邻2项和
lst = [1, 4, 9, 16, 2, 5, 10, 15]
l1 = []
for i in range(len(lst)-1):
    # if i < len(lst)-1:
    l1.append(lst[i] + lst[i+1])
print(l1)

print([ lst[x] + lst[x+1] for x in range(len(lst)-1) ])


## 3.随机生成100个产品ID, ID格式: 000005.xcbaaduixy
import random
alphabat = range(97, 123) # a-z
for _ in range(1,6):
    s = ''.join([chr(i) for i in random.choices(alphabat, k=10)])
    print('{:06}.{}'.format(_, s))

# 生成字母表
import string
print(string.ascii_lowercase)