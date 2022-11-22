#!/usr/bin/env python
#-*- coding: utf-8 -*-

# argparse模块, 参数解析，3.2 新版功能.
# https://www.osgeo.cn/cpython/library/argparse.html

import sys
# print(sys.argv)   # 返回列表，arg[0]代表脚本本身

import argparse
# ls /etc
# ls -a -l -h /etc      ls -lha /etc     ls --all -h -l /etc
# ls -la -h /etc        ls /etc -la -h

# 获得一个参数解析器
parser = argparse.ArgumentParser(prog='ls', add_help=False, description='lsit director contents')
parser.add_argument('path', nargs='?', default='.', help='dir name')            # 位置参数 ? * +(不需要缺省值)
parser.add_argument('-a', '--all', action='store_true', help='show all files')  # - 选项参数 store_true(给参数为True), 对应的store_false
parser.add_argument('-h', action='store_true', help='siamle read')   # 与系统默认 -h 打印帮助冲突，修改 add_help=False
parser.add_argument('-l', dest='long', action='store_true', help='long format string')  # 自定义参数名：dest='long'
# parser.print_help()   # 打印帮助信息，默认: add_help=True, -h --help

script_name = parser.prog  # ls, 程序名字，缺省: sys.argc[0] 或 basename

# 模拟传递参数
'''
args = parser.parse_args(['/etc', '-ah'])      # 传入可迭代对象: ('/etc',) , 接收 sys.argv 参数列表
print(type(args), args, args.long, args.path)  # 打印接收到的参数
# Namespace(path='/etc', all=True, h=True, long=False) False /etc
'''


# 练习

## ls 业务功能实现
# ls -l  详细
# ls -a  隐藏
# ls -r  排序
# ls -h  可读 (结合-l)

import stat
import argparse
from pathlib import Path
from datetime import datetime

# 获得一个参数解析器
parser = argparse.ArgumentParser(prog='ls', add_help=False, description='list directory contents')
parser.add_argument('path', nargs='?', default='.', help='directory')
parser.add_argument('-l', action='store_true', dest='long', help='use a long listing format')
parser.add_argument('-a', '--all', action='store_true', help='show all files, do not ignore entries staring with .')
parser.add_argument('-r', '--reverse', action='store_true', help='reverse order while strting')
parser.add_argument('-h', '--human-readable', action='store_true', dest='human', help='with -l, print sizes in human readable format')
# args  = parser.parse_args()  # 分析参数，传入可迭代参数
# print(args)  # 打印收集的参数
# parser.print_help()  # 打印帮助

'''
# ls /etc
def listdir(path, all=False):
    """列出当前目录文件"""
    p = Path(path)
    # for f in p.iterdir():
        # if not all and f.name.startswith('.'):  # 不显示隐藏文件
        #     continue
        # yield f.name
    # yield from filter(lambda f: not(not all and f.name.startswith('.')), p.iterdir())
    yield from map(lambda x: x.name, filter(lambda f: all or not f.name.startswith('.'), p.iterdir()))  # 路径转换为字符串

# print(*listdir(args.path), sep='\n')


# ls -l /etc
# drwxr-xr-x  11 flybird  staff   352 Feb 26 09:57 demo
def listdirdetail(path, all=False):
    """详细列出目录"""
    p = Path(path)
    for f in p.iterdir():
        if not all and f.name.startswith('.'):
            continue
        # mode 硬链接 属主 属组 字节 时间 name
        st = f.stat()
        import stat
        mode = stat.filemode(st.st_mode)  # st_mode是整数，理由stat函数，转换为八进制描述权限，最终显示 rwx 格式
        mtime = datetime.fromtimestamp(st.st_mtime).strftime('%Y-%m-%d %T')
        yield (mode, st.st_nlink, st.st_uid, st.st_gid, st.st_size, mtime, f.name)

print(*listdirdetail(args.path), sep='\n')
# 'drwxr-xr-x', 1, 1000, 1000, 352, '2022-02-26 01:57:38', 'demo'
'''




# 最终合并代码

def _gethuman(size: int):
    """单位转换"""
    units = ' KMGTP'
    depth = 0
    while size > 1000 and depth < len(units) - 1:
        # 当前size大于1000, 且depth不是最后一个进入循环
        depth +=1
        size //= 1000
    return '{}{}'.format(size, units[depth] if depth else '')

def _listdir(path, all, detail, reverse, human):
    """详细列出本目录"""
    p = Path(path)
    for i in p.iterdir():
        if not all and i.name.startswith('.'):
            continue
        if not detail:
            yield (i.name)
        else:
            st = i.stat()
            mode = stat.filemode(st.st_mode)  # st_mode是整数，理由stat函数，转换为八进制描述权限，最终显示 rwx 格式
            mtime = datetime.fromtimestamp(st.st_mtime).strftime('%Y-%m-%d %T')
            size = st.st_size if not human else _gethuman(st.st_size)
            # '-rw-r--r--', 1, 1000, 1000, '5K', '2022-04-17 10:09:14', 'test.py'
            yield (mode, st.st_nlink, st.st_uid, st.st_gid, size, mtime, i.name)

def listdir(path, all=False, detail=False, reverse=False, human=False):
    """根据文件名称排序"""
    return sorted(_listdir(path, all, detail, reverse, human), key=lambda x:x[len(x)-1], reverse=reverse)

if __name__ == '__main__':
    # args = parser.parse_args('-lrha'.split())  # 分析参数，同时传入可迭代的参数
    args = parser.parse_args()
    print(args)
    parser.print_help()
    print('-'*50)
    files = listdir(args.path, args.all, args.long, args.reverse, args.human)
    print(*files, sep='\n')

# 测试：
# python xxx.py -lha -r
# python xxx.py /etc -lhar