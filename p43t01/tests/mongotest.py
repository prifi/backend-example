#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author:flybird 2022/09/11

"""
import pymongo

# 建立连接
# username, password
client = pymongo.MongoClient('127.0.0.1', 27017)
print(client, type(client))

# 访问集合
db = client.mytest
users = db.users
print(*users.find())

# 关闭连接
client.close()
"""


# ODM -> 对象文档映射
# MongoEngine
from mongoengine import connect
from mongoengine import (
    Document,
    StringField,
    IntField
)

# 建立连接
conn = connect(db='mytest', host='127.0.0.1', port=27017)  # 配置文件读取

# Model类，字段(需要先建立连接 conn)
class User(Document): # BlogUser -> blog_user 集合名映射关系
    meta = {'collection': 'users'}  # 手动指定集合
    name = StringField(required=True, max_length=24)
    age = IntField(min_value=0, max_value=150, default=20)

    def __str__(self):
        return "<U, {}, {}, {}>".format(self.pk, self.name, self.age)


# ---- 查 ----
User.objects.all()
for u in User.objects:
    print(u.pk, u.id, u.name, u.age)
    print(u)

## 查一个
User.objects.get(name='tom')
User.objects(age__gte=20).first()
User.objects(name='tom').get()     # 返回多个异常 -> MultipleObjectsReturned

## 查多个，过滤
User.objects(age__not__gt=30)
User.objects(name__not__istartswith='xiao')


# ---- 增 ----
## create
u1 = User.objects.create(name="jerry", age=32)
print(type(u1), u1)

## save
u2 = User(name='t')
u2.name = 'tom'
u2.save()
print(type(u2), u2)


# ---- 排序 ----
User.objects.order_by('-pk')


# ---- 分页 ----
# first(), [0], limit(), skip()
# User.objects[2:4]
User.objects.order_by('-pk').limit(2).skip(2)


# ---- 聚合 ----
# count(), sum(), average()
User.objects(age__gte=30).average('age')  # 32.0 float


# ---- Q ----
User.objects(name='tom', age__lte=30)
print(*User.objects(Q(name='tom') & Q(age__gt=10)))
print(*User.objects(Q(name='tom') & Q(age__gt=10)))


# ---- 改 ----
user = User.objects.get(name='xiaopf')
user.age += 20
user.save()

# update, update_one 更新多个或一个
User.objects.filter(name='tom').update(age=10)
User.objects(name='tom').update_one(age=20)

user = User.objects.get(name='xiaopf')
User.objects(name='xiaopf').update_one(inc__age=50)  # 年龄加50
user.reload()  # 注意reload


# ---- 删 ----
User.objects(age__in=[20, 60]).delete()
