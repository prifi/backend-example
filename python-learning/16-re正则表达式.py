#!usr/bin/env python
# -*- coding:utf-8 -*-
"""
@version:
author:fly
@time: 2021/03/09
@file: re正则表达式.py
@function:
@modify:
"""

# 正则表达式

# 正则表达式30分钟入门教程: https://www.w3cschool.cn/regex_rmjc/
# 正则表达式语言 - 快速参考: https://docs.microsoft.com/zh-cn/dotnet/standard/base-types/regular-expression-language-quick-reference?redirectedfrom=MSDN
# 测试正则：https://regex101.com/

# 元字符
'''
^ $       # 锚定行首行尾
\b        # 锚定单词开头结尾
\d \D     # 数字
\w \W     # 字母数字汉字下划线
\s \S     # 任意空字符 \n \t \v \r\n
? . + *   # 0or1 1or多 0or多
() [] {}  # 分组 或 次数
? (非贪婪) # 在重复元字符后
[^]       # 非 

# [a-zA-Z\_][0-9a-zA-Z\_]{0, 19} # 精确地限制了变量的长度是1-20个字符
'''

# 或
'''
# 匹配电话
    # 025-83105736
    # 0543-5467328

(?:\d{3}|\d{4})-?\d{7,8}
'''

# 分组
'''
(pattern) 从1开始, group(1)
    # took look wood food

(?:t|l)(oo)k          # (?:)  取消分组号，group(1) 为 oo
(?:t|l)(?<name>oo)k   # (?<>) 命名分组  Python re库需要加P: (?P<>)

# 分组引用 \数字
    # very very vary sorry
(v\w+y) \1   # 匹配 very very
'''

# 断言 pyhon re库不支持
'''
if 的作用，条件，不占用分组号，如果后面或前面怎么怎么样就匹配 ...

ve(?=ry\b)  # 后面如果结尾是ry的匹配，very 匹配到 ve, 
(?<=\bf)ood # 前面如果以f开头的匹配，food 匹配 ood
(?!exp)   # 匹配的后面不能够是xx
(?<!exp)  # 匹配的前面不能够是xx
'''

# 贪婪与非贪婪
'''
v.*?y  # 在重复符号后面加?，尽量少匹配
'''

# 其他选项
'''
普通模式：就是一个长长的字符串  re.I 忽略大小写
多行模式：普通模式改成以\n为换行符的多行文本，只影响^$  re.M
单行模式：DOT ALL，. 点一穿到底  re.S

.   任意一个字符，不能是\n，普通模式，多行模式。
    单行模式，dot all \n 也能匹配

^ 永远指的是行首
$ 永远指的是行尾 
    ^\w+$       # 中间不包含空格，一行既是开头，又是结尾
        123     # 匹配
        123 abc # 不匹配
'''


# Python re模块
import re

'''
# 匹配上返回match对象（前包后不包），无匹配返回 None
re.compile     # 编译，支持 position:前包后不包，*推荐提前编译
re.match       # 开头匹配 单次* 
re.search      # 全文匹配 单次* 
re.fullmatch   # 完全匹配  funmatch(r'xxx', 7, 10) 子串也需要完全匹配  单次* 
re.findall     # 全文搜索 返回列表 元素是str
re.finditer    # 全文搜索 返回迭代器 元素是match对象
re.sub         # 替换，匹配到的全替换，count:最大替换几次
'''

# 全文搜索
s='''bottle\nbag\nbig\nable\na'''
regex = re.compile(r'b\w+', re.S)
r = regex.finditer(s)
for m in r:
    print(m, m[0], m.start(), m.end(), m.string[m.start():m.end()])


# 判断正则是否匹配
test = '用户输入的字符串'
if re.match(r'正则表达式', test):
    print('ok')
else:
    print('failed')
# 结果：failed


# 正则切分字符串
x = re.split(r'\s+', 'a b  c')  # 忽略连续空格 ['a', 'b', 'c']
y = re.split(r'[\s\,\;]+', 'a,b c; d')      # 忽略空格逗号分好 ['a', 'b', 'c', 'd']
# (*filter(None, re.split('[.(),\s]+', s))  # 忽略空格并解构


# 分组 group()
m = re.match(r'^(?P<p1>\d{3})-(?P<p2>\d{3,8})$', '010-12345')
print(m)
print(m.groups())  # ('010', '12345')
print(m.group())   # 010-12345  # 默认group(0) 本身,匹配从索引1开始
print(m.group(1))  # 010
print(m.group('p1'))
print(m.groupdict())  # {'p1': '010', 'p2': '12345'}  # 转换为字典


# 提取时间
'''
t = '19:05:30'
m = re.match(r'^(0[0-9]|1[0-9]|2[0-3]|[0-9])\:(0[0-9]|1[0-9]|2[0-9]|3[0-9]|4[0-9]|5[0-9]|[0-9])\:(0[0-9]|1[0-9]|2[0-9]|3[0-9]|4[0-9]|5[0-9]|[0-9])$', t)
m.groups()
---
('19', '05', '30')
'''


# 贪婪匹配 +? *? 尽可能少的匹配
## 需求匹配'102300'数字后面的0
r = re.match(r'^(\d+)(0*)$', '102300').groups()
print(r)  # ('102300', '')

# 非贪婪模式
r1 = re.match(r'^(\d+?)(0*)$', '102300').groups()
print(r1)  # ('1023', '00')


# 编译 *
## 使用编译后的正则表达式去匹配字符串，效率更高（预编译 re.compile()）
re_telephone = re.compile(r'^(\d{3})-(\d{3,8})$')
print(re_telephone.match('010-12345').groups())
print(re_telephone.match('010-123'))



# 练习

## 匹配数字 0~99, 100~999 不包括 0x? 开头的
'''
(?:[1-9]\d?\d|[1-9]?\d)(?!\d+)    # 注意 9999
(?:[1-9]\d{0,2}|0)
'''


## 匹配IP, 验证交给IP地址库socket模块
'''
(?:\d{1,3}\.){3}(\d{1,3})
(:?25[0-5]|2[0-4]\d|[01]?\d\d?\.){3}(:?25[0-5]|2[0-4]\d|[01]?\d\d?)  # 更精确的过滤

import socket
ip = '255.168.12.1'
nw = socket.inet_aton(ip)  # 错误抛异常
print(nw, socket.inet_ntoa(nw))
'''


## 提取文件名
# ftp://ftp/ascas/cp/pub/file/file-5.14.tar.gz
'''
.*ftp.*/(?P<filename>[^/\s]+\.(?:xz|gz))   # 命名分组
'''


## 提取html <a>标签内容
# <a herf='http://www.baidu.com' target='_blank'> 分组引用 <a>test </a>
'''
<(\w+)>(.+)</\1>
'''


## 提取html中herf后面的链接
'''
.*herf\s*=\s*[\'\"]?([^\s\'\"<>]+).*
'''


## 尝试写一个验证Email地址的正则表达式。版本一应该可以验证出类似的Email
import re

def is_valid_email(addr):
    re_email = re.compile(r'^\w[\w\.]+@\w[\w\-\.]*(?:\w+)+')
    return re_email.match(addr)

assert is_valid_email('someone@gmail.com')
assert is_valid_email('bill.gates@microsoft.com')
assert not is_valid_email('bob#example.com')
assert not is_valid_email('mr-bob@example.com')
print('ok')


## 提取出带名字的Email地址
import re
def name_of_email(addr):
    re_name = re.compile(r'<(\w+\s\w+)>|\w+')
    if re_name.match(addr).groups()[0]:
        return re_name.match(addr).group(1)
    return re_name.match(addr).group(0)
assert name_of_email('<Tom Paris> tom@voyager.org') == 'Tom Paris'
assert name_of_email('tom@voyager.org') == 'tom'
print('ok')

# re_name = re.compile(r'<(\w+\s\w+)>|\w+')
# print(re_name.match('<Tom Paris> tom@voyager.org').groups()[0])
# print(re_name.match('tom@voyager.org').groups()[0])

# 方法2：
print([x for x in re.split(r'[\<\>\@]+', '<Tom Paris> tom@voyager.org') if x][0])
print([x for x in re.split(r'[\<\>\@]+', 'tom@voyager.org')][0])


## 检索和替换  re.sub
# re.sub(pattern, repl, string, count=0, flags=0)
    # flag
        # re.I 忽略大小写
        # re.M 多行模式

phone = "2004-959-559 # 这是一个国外电话号码"

# 删除字符串中的 Python注释
re.sub(r'#.*$|\s+', "", phone)   # 2004-959-559

# 删除非数字(-)的字符串
re.sub(r'\D', "", phone)   # 2004959559


## (?P<>...)' 分组匹配
s = '1102231990xxxxxxxx'
res = re.search('(?P<province>\d{3})(?P<city>\d{3})(?P<born_year>\d{4})',s)
print(res.groupdict())
# {'province': '110', 'city': '223', 'born_year': '1990'}