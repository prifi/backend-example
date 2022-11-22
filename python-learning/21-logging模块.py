#!/usr/bin/env python
#-*- coding: utf-8 -*-

# logging 日志模块


# 日志层级，级别，根

import logging

# 获取root方式
# root = logging.root
# root = logging.Logger.root
root = logging.getLogger()     # "root"


# logging.info('test info ~~~')
# logging.warning('test warning ~~~')


# 日志记录器，创建日志实例
log1 = logging.getLogger('m1')
print(log1, type(log1))
print(log1.parent, log1.parent is root)  # 父  <RootLogger root (WARNING)> True


log4 = logging.getLogger('m1.m2')   # 子  . 表示日志层级结构
print(log4.name, log4.parent, log1 is log4.parent)   # m1.m2 <Logger m1 (WARNING)> True


# 日志级别
    # NOTSET 0 表示未定义
    # DEBUG,INFO,WARNING,ERROR,CRITICAL 10 - 50
    # root 30，默认WARNING

log = logging.getLogger('m1')   # 默认消息级别 NOTSET, 0
# log.setLevel(40)     # 手动设置消息日志有效级别
print(log.level, log.getEffectiveLevel())  # 日志有效级别
log.info('log test info ~~~')         # 不能输出，msg 20 < log Effective level (root, 30) 默认会去继承离他最新的父日志级别level
log.warning('log test warning ~~~')   # 可以输出，msg 30 == log Effective level (root, 30) 默认会去继承离他最新的父日志级别level


# ** log消息级别 >= log有效级别，才有输出机会，如果没有配置level会去找离他最近的父日志级别有效level **


# 日志根root输出格式 basicConfig   ==> ** 注意先配置，后使用！！本质上是对根记录器做最基本配置 **
from datetime import datetime, timedelta
def beijing(sec, what):
    "日志时间转换为北京时间输出"
    beijing_time = datetime.now() + timedelta(hours=8)
    return beijing_time.timetuple()
logging.Formatter.converter = beijing
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',)
                    # 输出日志到日志文件
                    # filename=logname,
                    # filemode='a')
logging.info('basicConfig ~~~')
log.warning('222')   # log实例都是继承自Logger的日志格式配置


# ** baseicConfig 函数执行完成后，会为root提供一个处理器，那么basicConfig函数就不能再调用了 **


# 处理器Handler
    # Handler控制日志信息输出目的地，可以是控制台、文件
        # 可单独设置level
        # 可单独设置格式
        # 可设置过滤器
    # basicConfig函数执行后，默认会生成一个StreamHandler实例，如果设置了filename，则只会生成一个FileHandler实例 => Root生效
import sys
FORMAT = '[%(asctime)s] %(filename)s[line:%(lineno)d] %(levelname)s %(message)s'
logging.basicConfig(
                    # level=logging.INFO,       # baseicConfig 只能用一次，后面再定义也没有用了
                    format=FORMAT,
                    # datefmt='%Y-%m-%d %H:%M:%S',)
                    # stream=sys.stderr,)
                    # 输出日志到日志文件
                    #filename='test.log',
                    #filemode='a'
                )

# 日志实例化
# root = logging.getLogger()

# 设置stream Handler
# h1 = logging.StreamHandler(stream=sys.stderr)     # 控制台输出
h2 = logging.FileHandler('test.log')                # 控制台和文件同时输出
# root.addHandler(h1)


# 给h1实例设置日志格式
f1 = logging.Formatter(FORMAT,datefmt='%Y-%m-%d %H:%M:%S')
h2.setFormatter(f1)     # ** 一个hander只能设置一个格式化字符串 **
# h1.setLevel(40)       # 日志消息级别小于Handler级别将不会被输出

# print(root.handlers)
# logging.info('test')   # msg level >= root EL; => all Handlers

log1 = logging.getLogger(__name__)
log1.propagate = True   # 阻断向上传播到父级日志
print(log1.parent, log1.level, log1.getEffectiveLevel(), log1.name)


# 给日志实例添加Handler
log1.addHandler(h2)    # ** 一个log可以设置多个handler **
print(log1.handlers)


# 日志轮转, 按照文件大小、时间间隔轮转 s,m,d interval
from logging import handlers
h3 = handlers.TimedRotatingFileHandler('test1.log', 'd', 1)
h3.setFormatter(logging.Formatter(FORMAT,datefmt='%Y-%m-%d %H:%M:%S'))
log1.addHandler(h3)


log1.warning('test')   # msg level >= log1.EL 资格有了，log1.handlers，发现root也打印了  => 日志流
    # ** test **
    # [2022-05-02 03:22:35,609] test.py[line:41] WARNING test


# 格式化器 Formartter
    # 按照记录器上的处理器上的设置的格式化器的格式字符串输出日志信息
    # 如果处理器上没有设置格式化器，会调用缺省 _defaultFromat  => '%(message)s'
# 定义格式化器
formatter = logging.Formatter('#%(asctime)s <%(message)s>#')
# 为处理器设置格式化器
# handler.setFormatter(formatter)



# 日志流

    # 1.消息level与当前logger的EffectiveLevel比较，小于结束，大于等于输出到所有handler处理
    # 2.消息记录级别与handler级别相比，低的不处理，高的输出
    # 3.当前logger所有handler处理完成后，向上传播(propagate)属性是否为True(缺省)
        # True: 传递到父logger，** 不需要和父logger的level比较 **，直接交给父的所有handler,重复2、3步骤，直到父logger是None退出


# 日志示例
import logging
# 根logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(threadName)s [%(message)s]",  # 设置消息输出格式
    datefmt='%Y-%m-%d %H:%M:%S',
)
print(logging.root.handlers)  # [<StreamHandler <stderr> (NOTSET)>]

mylogger = logging.getLogger(__name__)  # level为0
mylogger.info('my info ~~~')   # 实际上传播给了root输出
print('-'*50)

# 定义处理器，输出到文件，按日期轮转
# handler = logging.FileHandler()
from logging import handlers
handler = handlers.TimedRotatingFileHandler('test.log', 'd', 1)
# handler = handlers.RotatingFileHandler('test.log', 'a', 1)
handler.setLevel(logging.WARNING)   # 设置处理器级别

# 定义格式化器
formatter = logging.Formatter('#%(asctime)s %(levelname)s <%(message)s>#', datefmt='%Y-%m-%d %H:%M:%S')

# 为处理器设置格式化器
handler.setFormatter(formatter)

# 为日志记录器增加处理器
mylogger.addHandler(handler)

print(mylogger.handlers)
mylogger.info('my info2 ~~~')   # info级别只会输出到控制台(root打印)，不会记录到文件

# 阻断向父logger传播，控制台不会再打印
mylogger.propagate = False
mylogger.warning('my info3 ~~~')   # 只会输出到文件