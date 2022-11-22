#!usr/bin/env python
# -*- coding:utf-8 -*-
"""
@version:
author:fly
@time: 2021/03/09
@file: collections.py
@function:
@modify:
"""
### collectons
# collections是Python内建的一个集合模块，提供了许多有用的集合类。

## 1.namedtuple
# 自定义tuple对象，规定tuple元素个数，通过属性引用tuple某个元素，具有tuple特性（不可变）
from collections import namedtuple

# namedtuple('名称', [属性list]):
Point = namedtuple('Point', ['x', 'y'])
p = Point(1, 2)
print(p.x, p.y)  # 1 2

# 验证Point对象是tuple子类：
isinstance(p, Point)  # True
isinstance(p, tuple)  # True

## 2.deque
# list线性存储，数据量大时插入删除效率低，deque高效实现插入和删除操作的双向列表，适合队列和栈
# 高效头部追加和删除元素
from collections import deque

q = deque(['a', 'b', 'c'])
q.append('x')
q.appendleft('y')
print(q)  # deque(['y', 'a', 'b', 'c', 'x'])
print(q.popleft())  # y 从左边弹出
print(q)  # deque(['a', 'b', 'c', 'x'])

## 3.defaultdict
# key不存在时，返回一个默认值，就可以用defaultdict
from collections import defaultdict

# 函数在创建defaultdict时传入，除了返回默认值其他行为与dict一致
dd = defaultdict(lambda: 'N/A')
dd['key1'] = 'abc'
print(dd['key1'])  # abc
print(dd['key2'])  # N/A   # key不存在

d = {'k': '1'}
print(d.get('k1', 'N/A'))  # N/A   # key不存在，同样效果

## 4.OrderedDict
# 对dict做迭代时，使key有序
from collections import OrderedDict

d = dict([('a', 1), ('b', 2), ('c', 3)])
print(d)  # {'a': 1, 'b': 2, 'c': 3}
od = OrderedDict([('a', 1), ('b', 2), ('c', 3)])
print(od)  # OrderedDict([('a', 1), ('b', 2), ('c', 3)])


## 5.ChainMap
# 逻辑上一组dict，查找时会按照顺序在内部dict依次查找，例如：既有默认参数又有环境变量的场景，设置参数优先级
from collections import ChainMap
import os, argparse

def chain_test():
    # 构造缺省参数:
    defaults = {
        'color': 'red',
        'user': 'guest'
    }

    # 构造命令行参数:
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--user')
    parser.add_argument('-c', '--color')
    namespace = parser.parse_args()
    command_line_args = { k: v for k, v in vars(namespace).items() if v }

    # 组合成ChainMap:
    combined = ChainMap(command_line_args, os.environ, defaults)

    # 打印参数:
    print('color=%s' % combined['color'])
    print('user=%s' % combined['user'])
'''
没有任何参数时，打印出默认参数：

$ python3 use_chainmap.py 
color=red
user=guest
当传入命令行参数时，优先使用命令行参数：

$ python3 use_chainmap.py -u bob
color=red
user=bob
同时传入命令行参数和环境变量，命令行参数的优先级较高：

$ user=admin color=green python3 use_chainmap.py -u bob
color=green
user=bob
'''


## 6.Counter
# 计数器，统计字符出现的个数
from collections import Counter
c = Counter()
for ch in 'porgramming':
    c[ch] = c[ch] + 1

print(c)
c.update('hello')
print(c)
# 结果
# Counter({'r': 2, 'g': 2, 'm': 2, 'p': 1, 'o': 1, 'a': 1, 'i': 1, 'n': 1})
# Counter({'o': 2, 'r': 2, 'g': 2, 'm': 2, 'l': 2, 'p': 1, 'a': 1, 'i': 1, 'n': 1, 'h': 1, 'e': 1})