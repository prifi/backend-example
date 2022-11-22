#!/usr/bin/env python
#-*- coding: utf-8 -*-

# 模块化


## 代码组织方式

# import os  # 'os' os是标识符，指向os模块对象
# import os.path  # ps
# import os.path as osp  # osp => path模块
# import pathlib  # import 之后必须是模块类型，.py或者目录

# print(__name__)
# print(type(osp))

# from pathlib import Path  # Path 类
# from os import path   # path 模块
# from functools import update_wrapper as uw, wraps as wr   # uw wr 函数
# from logging import root   # logging 全局比那里
# from os.path import exists  # exists


# from 模块 import 函数、类、变量、模块、*
    # from 后面只能导入模块，import 后面可以是任意


# from pathlib import *   # * 批量导入

print(*dir(), sep=',')              # 当前环境的所有变量，全局
print(*sorted(globals().keys()), sep=',')   # 全局环境
print(*sorted(locals().keys()), sep=',')    # 局部环境



# 自定义模块命名规范
    # 标识符要求，全小写，下划线分割，避免与内建函数冲突


# 模块搜索顺序，从前到后，从左到右，可以修改：sys.path.inert(0, path)
import sys
# print(*sys.path, sep='\n')    # 程序主目录，PYTHONPATH目录，标准库目录


# 模块重复导入
    # 所有已经加载的模块都会记录在sys.modules中，sys.modules是存储已经加载过的所有模块的字典
# print(*sys.modules.items(), sep='\n')


# if __name__ == '__main__' 用途
    # 对于非主模块，测试本模块内的函数，类
    # 避免主模块变更的副作用




# 包

# 模块要用必须加载，应该在sys.modules看到
# 目录下 __init__.py  采用最小加载原则, m.__file__ 指向 __init__.py 文件路径
# dir(m)
# m.__dict__
# import m.X
# import m.m1


# import os
# os.path.exists('.')
# import sys
# print(sys.modules.keys())

# 模块和包的总结：
    # 导入子模块一定会加载父模块，导入父模块不一定会导入子模块

from json import encoder  # json.dump , 无法使用
import json.encoder       # json.dum , 可以使用


import sys

# import m
# import m.m1
# from m import m1

# import m.m2.m21

# from m.m2 import m22
# import m
# m.m2.Z        # 导入了m才能使用 m.m2 标识符

print('-'*30)
print(*filter(lambda x: x.startswith('m'), dir()))

print('-'*30)
print(sorted(filter(lambda x:x.startswith('m'), sys.modules.keys())))





# 绝对导入、相对导入

# 包内使用，不要在顶层模块中使用相对导入，顶层使用绝度导入
    # . 当前目录
    # .. 表示上一级
    # ...

# import .m   import 语句不能使用相对导入，在包里面用相对导入，避免因路径改名引起不可用
# from .m import m1  相对导入不要用在包之外，不能当做主模块(__main__)运行

# 举例，a.b.c 模块，a、b是目录，c是模块c.py
# c代码如下：
    # from . import d    # import a.b.d
    # from .. import e   # import a.e
    # from .d import x   # a.b.d.x
    # from ..e import x  # a.e.x


# __init__.py 使用相对的点号，按目录的层次来
# 非 __init__.py 文件层次与逻辑层次一致




# 访问控制

# import t1
# from t11 import X, _B as b, __C
# from t1 import *   # 默认下划线开头的不能导入；如果t1有 __all__ = ["Point"], 则它说了算

import m.m1
print(getattr(m.m1, 'X'))




# 源代码打包分发

# from distutils.core import setup
from setuptools import setup   # 支持wheel, egg

# setup.py
# python setup.py --help-commands
# python setup build    # 执行编译
setup(
    name = 'm',
    version = '0.1.1',
    description = 'm tool',
    author = 'xiaopf',
    anthor_email = 'xiaopf@example.com',
    url = 'www.xiaopf.com',
    packages = ['m', 'm.m2', 'm.m2.m21'],   # 包相关的，'m'包自身和非子包，必须是包或py文件
    py_modules = ['t2'],    # 模块相关，'t2.py' 必须是模块
    data_files = [          # 文件相关，依赖文件以及第三方文件
        ('install', ['requirements' ]),
        ('htmls', [])
    ],
    python_requires = ">3.6"   # pip install 会检查python版本是否符合要求
)

# build 生成一个build目录，编译好文件和目录
# sdist: 先build, 然后source Distribute打包, tar.gz 格式(--formats=gztar,zip)
    # sys.path.insert(0, os.path.abspath('.'))


# 二进制打包成wheel包分发
    # pip install wheel
    # python setup.py bdist_wheel   # pip install xxx.whl    # 需要自行解决依赖问题，可连依赖包一起安装
