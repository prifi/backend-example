#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author:flybird 2022/09/10

# https://github.com/pypa/sampleproject/blob/main/setup.py

from setuptools import setup, find_packages

setup(
    name="myproject",
    version="1.0",
    author="fly",
    author_email="admin@example.com",
    description="Learn to Pack Python Module",
    url="http://python.org/",

    # 额外参数
    packages=find_packages(),  # 包和包下的.py文件打包
    py_modules = ['manage'],   # manage.py
    python_requires=">=3.6",   # 要求python版本
    data_files=[('', ['requirements'])], # 打包文件

    # # 用来支持自动生成脚本，安装后会自动生成 /usr/bin/foo 的可执行文件
    # # 该文件入口指向 foo/main.py 的main 函数
    # entry_points={
    #     'console_scripts': [
    #         'foo = foo.main:main'
    #     ]
    # },
    #
    # # 将 bin/foo.sh 和 bar.py 脚本，生成到系统 PATH中
    # # 执行 python setup.py install 后
    # # 会生成 如 /usr/bin/foo.sh 和 如 /usr/bin/bar.py
    # scripts=['bin/foo.sh', 'bar.py']
)

# 打包命令：python setup.py sdist --formats=gztar
