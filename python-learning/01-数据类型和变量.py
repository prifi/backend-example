#!usr/bin/env python
# -*- coding:utf-8 _*-
"""
@version:
author:xiaopengfei
@time: 2021/01/24
@file: 01-数据类型和变量.py
@function:
@modify:
"""

## 输入输出
print('hello world')
print('100 + 200 = ', 100 + 200)

# 输出打印
# name = input()
# print(name)


## 数据类型
# 包括：整数、浮点数、字符串、布尔值、空值、变量、常量

# 字符串
# 转义
print('I\'m \"OK\"!')  # I'm "OK"

# r'xx' 表示默认不转义
print(r'\\\t')  # \\\t

# ''' 打印多行内容, 加 r''' 表示默认不转义\n会原样输出
print(r''' \n
line1
line2
''')

# 布尔值 True False
# and or not
print(5 > 3 and 3 > 1)  # True

# 空值 None or 0
# None不能理解为 0
print(None)

# 变量
# 大小写英文（大小写敏感）、数字和_的组合，且不能用数字开头
a = 'low'
A = 'high'
print(a, A) # low high

# 常量
    # 在Python中，通常用全部大写的变量名表示常量
PI = 3.1415926
print("除法运算： ",10 / 3)          # 3.3333333333333335
print("板除运算（取整）：", 10 // 3)  # 3
print("余数运算（取余）：", 10 % 3)   # 1  # 无论整数做//除法还是取余数，结果永远是整数 10 % 3 = 9 .. 1


# 编码介绍
    # ASCII 1byte = 8bit = 255, 2byte = 65535
    # Unicode 2byte（特殊生僻4byte）
    # Utf-8 可变长编码1~6byte，英文存储1byte，汉字存储3byte（生僻4-6个字节)
# 在计算机内存中，统一使用Unicode编码，当需要保存到硬盘或者需要传输的时候，就转换为UTF-8编码。
    # - 文件读取的UTF-8字符被转换为Unicode字符到内存里，编辑完成后，保存的时候再把Unicode转换为UTF-8保存到文件;
    # - 浏览网页的时候，服务器会把动态生成的Unicode内容转换为UTF-8再传输到浏览器

# 字符串
    # Python 3版本中，字符串是以Unicode编码的

print('中文str')
print(ord('A'))  # 65  # ord()转换字符串整数表示
print(chr(66))   # B   # chr()转换为字符串表示

print('\u4e2d\u6587')  # 中文 # 16进制表示

# Python对bytes类型的数据用带b前缀的单引号或双引号表示，如果要在网络上传输，或者保存到磁盘上，就需要把str变为以字节为单位的bytes。
# x,y虽然输出结果一样，但y是str，bytes的每个字符都只占用一个字节，y则为Unicode编码2字节
x = b'ABC'
y = 'ABC'

# 以Unicode表示的str通过encode()方法可以编码为指定的bytes，使用 encode() 方法
print('ABC'.encode('ascii'))    # b'ABC'
print('中文'.encode('utf-8'))    # b'\xe4\xb8\xad\xe6\x96\x87' # 在bytes中，无法显示为ASCII字符的字节，用\x##显示
# print('中文'.encode('ascii'))  # 错误：中文不能编码为ascii，UnicodeEncodeError: 'ascii' codec can't encode characters ...

# 反之，从网络或磁盘上读取了字节流（单位bytes），需要把bytes转换为str, 使用 decode() 方法
print(b'\xe4\xb8\xad\xe6\x96\x87'.decode('utf8'))  # 中文
print(b'\xe4\xb8\xad\xe6'.decode('utf8', errors='ignore'))  # 中 # errors,忽略无法解析的字节

# 计算字符或字节数 len()
print(len('ABC'), len('中文')) # 3 2
print(len('ABC'.encode('ascii')), len('中文'.encode('utf-8'))) # 3 6 # 可见，1个中文字符经过UTF-8编码后通常会占用3个字节，而1个英文字符只占用1个字节


# 格式化输出字符串
# % 占位符
print('Hello %s' % 'world!')
print('Hi %s, you age is %d.' % ('xiao', 18))
print('%2d-%02d' % (3, 1))  #  3-01 # 格式化输出及补0
print('%.2f' % 3.1415926)   # 3.14
print('%s%%' % 70)          # 70% # 两个%代表%本身输出

# .formant() 占位符{0}、{1}……
print('{0}成绩提升了{1:.2f}%'.format('小明', 17.125)) # 小明成绩提升了17.12%

# f-string
# 字符串如果包含变量{xxx}，就会以对应的变量替换
r = 2.5
s = 3.14 * r ** 2
print(f'{r} {s:.2f}')  # 2.5 19.62

## 练习1：输入半径求面积
r = float(input('输入半径：'))
c = 3.1415926 * r * r
print('%.2f' % c)