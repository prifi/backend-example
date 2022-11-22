#!/usr/bin/env python
# -*- coding: utf-8 -*-

# PyMySQL

import simplejson
import pymysql
from pymysql.cursors import DictCursor   # 获取字典 {}, [{}, {}]

with open('conf.json', encoding='utf-8') as f:
    conf = simplejson.load(f)

conn = None
cursor = None
try:

    conn = pymysql.connect(**conf)
    cursor = conn.cursor(DictCursor)     # 游标
    sql = 'select * from titles'
    x = cursor.execute(sql)

    # conn.commit()     # 持久化，增删改
    # print(x)          # 返回影响的行数

    print(cursor.rownumber, cursor.rowcount)   # 当前行，总行
    print(cursor.fetchone())                   # 取一条，不能回头，tuple
    print(cursor.fetchone())

    print(cursor.rownumber, cursor.rowcount)
    print(cursor.fetchall())                   # 获取剩下的，tuple

    cursor.rownumber = 0                       # 修改行号，重复获取
    print(cursor.rownumber, cursor.rowcount)
    print(cursor.fetchall())

except Exception as e:
    conn.rollback()   # 异常回滚，原子性

finally:
    if cursor:
        cursor.close()
    if conn:
        conn.close()



# 不建议拼接，建议 ** 参数化查询 ** 提高安全性
# SQL语句缓存
'''
user_id = '1 or 1'        # 短路，SQL注入攻击，查询出全部数据 
isql = """select * from titles where emp_no={}""".format(user_id)

--------

# 使用%s
user_id = '10001 or 1' 
isql = """select * from titles where emp_no=%s"""
x = cursor.execute(isql, user_id)

# 使用字典
isql = """select * from titles where name like %(name)s age > %(age)s"""   # 不推荐使用 like %..
x = cursor.execute(isql, {name: 'tom-%', 'age': 18})     # 注意模糊查询 %
'''


# 上下文管理
with open('conf.json', encoding='utf-8') as f:
    conf = simplejson.load(f)
try:
    conn = pymysql.connect(**conf)
    with conn:   # 离开时关闭连接
        try:
            with conn.cursor() as cursor:  # 离开时关闭cursor
                user_id = '10001 or 1'
                isql = """update student set xxx=xxx where emp_no=%s"""
                x = cursor.execute(isql, user_id)
                # conn.commit()
                print(x, cursor.fetchall())
            conn.commit()
        except:
            conn.rollback()   # 出异常回滚
except Exception as e:
    print(e)