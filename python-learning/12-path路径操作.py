#!/usr/bin/env python
#-*- coding: utf-8 -*-

# 路径操作
    # os.path
    # pathlib  --> 推荐

import os
from os import path

# 系统分隔符 /
print(os.sep)
print(path.sep)

# 拼接路径
p = path.join('/etc', 'sysconfig', 'network')
print(type(p), p)  # str /etc/sysconfig/network

# 分割路径
print(path.split(p))      # ('/etc/sysconfig', 'network')
print(path.splitdrive(p)) # Windows 分割驱动器 'D:/'
print(path.splitext('/root/test.py')) # 分割后缀 ('/root/test', '.py')
print(path.dirname(p))    # /etc/sysconfig
print(path.basename(p))   # network

# 是否存在
print(path.exists(p))      # True
print(path.isdir(p))
print(path.isfile(p))

print(path.abspath('test'))  # 绝对路径

# 应用
print(__name__)
print(__file__)
parent = os.path.dirname(__file__)  # 当前文件父路径
code_path = os.path.join(parent, 'code', 'app')  # 加入 code/app 路径
print(code_path)


print('-' * 30)


# Path 类（3.4）
from pathlib import Path
print(Path(), Path('magedu'), Path(''))

# 拼接路径
p = Path('/etc', 'sysconfig', 'network')
p.exists()
p.is_dir()
print(type(p), p)  # Path对象， <class 'pathlib.PosixPath'> /etc/sysconfig/network
# p.joinpath(*('a', 'b'))  -> 解构方式拼接路径

# 构建路径 注意与 Path 对象拼接
p1 = Path('/a', 'b', 'c/d', Path('e'), 'f/g')   # /a/b/c/d/e/f/g
p2 = Path('a') / 'b' / 'c/d'  # / 用来路径拼接  a/b/c/d
p3 = Path('a', Path('b/c')) / 'e/f'
p4 = 'a' / Path('b/c')  # a/b/c
# p5 = 'a'/ 'b/c' / Path('b/c')   # 报错，字符串不能拼接，用括号改变优先级

# 转换为路径字符串
str(p1)   # '/a/b/c/d/e/f/g'
repr(p1)  # PosixPath('/a/b/c/d/e/f/g')
# open(p1), open(str(p1))  # 打开一个文件

# 拿到路径分割各个部分
print(p1.parts)   # ('/', 'a', 'b', 'c', 'd', 'e', 'f', 'g')

# 拼接
print(p1.parent.parent / 'code/app')  # 父路径拼接
# p1.parents 迭代器，路径对象
# p1.parents[0]
# p1.parents[len(p1.parents)-1]  # 不能取负

p5 = p1.joinpath('aa' / Path('bb/cc') / 'mysql.tar.gz')
# p5 = p1.joinpath(*('bb/cc'))

# 基
print(p5.parent)  # /a/b/c/d/e/f/g/aa/bb/cc
print(p5.name)    # mysql.tar.gz
print(p5.suffix)  # .gz
print(p5.stem)    # mysql.tar
print(p5.with_suffix('.xz'))        # /a/b/c/d/e/f/g/aa/bb/cc/mysql.tar.xz
print(p5.with_name('mysql.ini'))    # /a/b/c/d/e/f/g/aa/bb/cc/mysql.ini

print(__file__)

# 全局方法
print(p5.home())  # 家目录
print(p5.cwd())   # 绝对路径
print(p5.cwd() / 'apps')

# 搜索 glob, rglob 返回生成器对象
p = Path(__file__).parent
print(list(p.glob('*.py')))     # 当前目录搜索
print(list(p.glob('**/*.??')))  # 递归 搜索后缀名为2个字符的文件，等同于 p.rglob('*.??')

# 其他实用方法
# p.parent.is_dir()  # 不递归，当前目录下文件或目录
# p.resolve()   # 仅适用于linux, 解析软链接的真正指向
# with p.open('rb') as f: pass
# p.replace(p1)
# p.mkdir(parents=True, exist_ok=True)  # touch, rmdir(空)
# p.rename(p1)

print('-'*30)

# 实例：遍历当前目录，返回其下文件，如果是目录，判断是否为空
for x in Path('tmp').iterdir():
    if x.is_dir():
        print(x.name, 'dir')
        for y in x.iterdir():
            print(x, 'not empty')
            break
        else:
            print(x.name, 'empty')
    else:
        print(x.name, 'other')


# 实例2: 递归查找文件，移动或重命名
def find_file(p):
    for file in p.iterdir():
        if file.suffix == '.sh':
            print(file.parent)
            break
        if file.is_dir():
            find_file(file)

for line in p1.glob('**/*.sh'):
    new_name = line.stem + '_test.sh'
    print(Path('/data') / new_name)


# 练习：编写一个程序，能在当前目录以及当前目录的所有子目录下查找文件名包含指定字符串的文件，并打印出相对路径。
import os
def find_file_path(i, dir):
    for x in os.listdir(dir):
        if os.path.isfile(os.path.join(dir, x)) and i in x:
            print(os.path.join(dir, x))
        if os.path.isdir(os.path.join(dir, x)):
            find_file_path(i, os.path.join(dir, x))
find_file_path('h', 'magedu')