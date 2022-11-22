#!usr/bin/env python
# -*- coding:utf-8 -*-
"""
@version:
author:fly
@time: 2021/03/09
@file: hashlib+hmac.py
@function:
@modify:
"""
### 摘要算法
# hashlib提供常见的摘要算法：MD5, SHA1等
# 特性：防篡改，单向加密
# 场景：登陆密码验证

## MD5
# MD5是最常见的摘要算法，速度很快，生成结果是固定的128 bit字节，通常用一个32位的16进制字符串表示。
import hashlib

md5 = hashlib.md5()
md5.update('hello'.encode('utf-8'))
# 数据量很大，可以分块多次调用update()，计算结果一致
md5.update('world'.encode('utf-8'))
print(md5.hexdigest())

## SHA1
# SHA1的结果是160 bit字节，通常用一个40位的16进制字符串表示。
import hashlib

sha1 = hashlib.sha1()
sha1.update('hello'.encode('utf-8'))
sha1.update('world'.encode('utf-8'))
print(sha1.hexdigest())

## 结果
# MD5:  fc5e038d38a57032085441e7fe7010b0
# SHA1: 6adfb183a4a2c94a2f92dab5ade762a47889a5a1

# 比SHA1更安全的算法是SHA256和SHA512，不过越安全的算法不仅越慢，而且摘要长度更长。


## 练习1：
# 根据用户输入的口令，计算出存储在数据库中的MD5口令进行验证：
import hashlib

db = {
    'michael': 'e10adc3949ba59abbe56e057f20f883e',
    'bob': '878ef96e86145580c38c87f0410ad153',
    'alice': '99b1c2188db85afee403b1536010c2c9'
}


def login(user, password):
    for u in db.keys():
        if u == user:
            return hashlib.md5(password.encode('utf-8')).hexdigest() == db[user]


# 测试:
assert login('michael', '123456')
assert login('bob', 'abc999')
assert login('alice', 'alice2008')
assert not login('michael', '1234567')
assert not login('bob', '123456')
assert not login('alice', 'Alice2008')
print('ok')

## “加盐”
# 通过对原始口令加一个复杂字符串来实现，俗称“加盐”
# 相同的口令生成同的MD5，通过把不可变登陆名作为salt一部分计算md5，实现相同口令存储不同的md5
db_1 = {}


def register(username, password):
    pass
    # db_1[username] = get_md5(password + username + 'the-Salt')


## 练习：根据用户输入的登录名和口令模拟用户注册，计算更安全的MD5：
# -*- coding: utf-8 -*-
import hashlib, random


def get_md5(s):
    # 计算md5
    return hashlib.md5(s.encode('utf-8')).hexdigest()


class User(object):
    def __init__(self, username, password):
        self.username = username
        # 加盐
        self.salt = ''.join(map(chr, random.choices(range(48,122), k=20)))
        self.password = get_md5(password + self.salt)


db_2 = {
    'michael': User('michael', '123456'),
    'bob': User('bob', 'abc999'),
    'alice': User('alice', 'alice2008')
}


def login(username, password):
    user = db_2[username]
    password += user.salt
    return user.password == get_md5(password)


# 测试:
assert login('michael', '123456')
assert login('bob', 'abc999')
assert login('alice', 'alice2008')
assert not login('michael', '1234567')
assert not login('bob', '123456')
assert not login('alice', 'Alice2008')
print('ok')




### hmac
# 通过一个标准算法，在计算哈希的过程中，把key混入计算过程中。

# 准备待计算的 [ 原始消息message，随机key，哈希算法 ]，这里采用MD5，使用hmac的代码如下：
'''
>>> import hmac
>>> message = b'Hello, world!'
>>> key = b'secret'
>>> h = hmac.new(key, message, digestmod='MD5')
>>> # 如果消息很长，可以多次调用h.update(msg)
>>> h.hexdigest()
'fa4ee7d173f2d97ee79022d1a7355bcf'
'''


## 练习：将上一节的salt改为标准的hmac算法，验证用户口令：
# -*- coding: utf-8 -*-
import hmac, random

def hmac_md5(key, s):
    return hmac.new(key.encode('utf-8'), s.encode('utf-8'), 'MD5').hexdigest()

class User(object):
    def __init__(self, username, password):
        self.username = username
        self.key = ''.join([chr(random.randint(48, 122)) for i in range(20)])
        self.password = hmac_md5(self.key, password)

db = {
    'michael': User('michael', '123456'),
    'bob': User('bob', 'abc999'),
    'alice': User('alice', 'alice2008')
}

def login(username, password):
    user = db[username]
    return user.password == hmac_md5(user.key, password)

# 测试:
assert login('michael', '123456')
assert login('bob', 'abc999')
assert login('alice', 'alice2008')
assert not login('michael', '1234567')
assert not login('bob', '123456')
assert not login('alice', 'Alice2008')
print('ok')