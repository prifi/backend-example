#!/usr/bin/env python
#-*- coding: utf-8 -*-

# 序列化和反序列化
import pickle

# Json 轻量级数据交换格式，文本序列化
        # 字符串、数值、true、false、null、对象、数组
        # 字符串必须使用双引号，不能是单引号

import json

d = {'name':'tom', 'age':20, 'interest':('movice', 'music'), 'class':['python']}

x = json.dumps(d, indent=4)
print(type(x), x, sep='\n')

d1 = json.loads(x)
print(d1)

# d 中元组转换回来成列表，json序列化不支持set集合
# {'name': 'tom', 'age': 20, 'interest': ['movice', 'music'], 'class': ['python']}

# d1 == d  # True
# d1 is d  # False


# JSON进阶
# class 序列化
class Student:
    def __init__(self, name, age, score):
        self.name = name
        self.age = age
        self.score = score

    def __str__(self):
        return '<{} {} {}>'.format(self.age, self.name, self.score)

s = Student('小明', 20, 88)

# 方法一：为对象专门写一个转换函数
def student2dict(std):
    return {
        'name': std.name,
        'age': std.age,
        'score': std.age
    }
print(json.dumps(s, default=student2dict))

# 方法二：直接使用实例字典  -> default
print(json.dumps(s.__dict__, ensure_ascii=False))       # {"name": "小明", "age": 20, "score": 88}
print(json.dumps(s, default=lambda obj: obj.__dict__))



# class 反序列化　　-> object_hook
def dict2student(d):
    return Student(d['name'], d['age'], d['score'])

json_str = '{"name": "Bob", "age": 20, "score": 88}'
print(json.loads(json_str, object_hook=dict2student))



# MsgePack 二进制序列化，占用空间和带宽更少
import msgpack

methods = (pickle, json, msgpack)  # 二进制、文本、二进制
for i,m in enumerate(methods):
    x = m.dumps(d)
    print(i+1, m.__name__, type(x), len(x), x)
print(msgpack.loads(x))