#!/usr/bin/env python
#-*- coding: utf-8 -*-

# 异常 Exception
    # 捕获异常原则：从小到大，从具体到宽泛，如果任何一个except语句捕获到异常，其他except语句就不会再次捕获了
    # 手动抛出异常：raise 后要求应该是BaseException类的子类或实例，如果是类将被无参实例化: raise IndexError('我抛出的异常的描述')
    # except中的 raise 将异常原样抛出（外层）
    # finally：最后一定要执行的，不管是否发生异常；一般放置资源的清理、释放工作的语句
        # finally 中有return,break语句，则异常不会继续向外抛出
    # else子句：必须写在 except 与 finally 之间；没有任何异常发生，则执行

# 自定义异常
class MyException(Exception):
    pass

import logging
import sys, time

FORMAT = "%(asctime)s %(name)s %(thread)d %(message)s"
logging.basicConfig(format=FORMAT, level=logging.INFO)

def foo():
    f = None
    try:
        # while 1:
        #     time.sleep(1)
        #     print('*'*30)
            # KeyboardInterrupt 捕获 Ctrl + C 异常
        # sys.exit(100)  # 系统退出异常(退出代码为 100)，结束当前解释器，属于BaseException子类
        # 1/0
        # 01 = 100   # 语法错误不会被捕获
        # raise ValueError()
        # rasise      # 错误
        try:
            f = open('text1.txt')
            print('$'*30)
        except:
            print('我什么都管')
            raise     # 正确，原样抛出异常，不处理异常
        raise MyException('异常原因')
        # raise 100  # isinstance(100, BaseException) => TypeError
        print('~'*30)
    except ZeroDivisionError:
        print('zero')
    except KeyboardInterrupt:  # 捕获异常并处理，不影响后续代码执行  isinstance(异常，Exception(BaseException))
        print('KeyboardInterrupt')
    except FileNotFoundError as e:  # 捕获自定义异常
        print('catch u', e, type(e), str(e), e.args)
        logging.error(e)   # 输出到错误日志
    else:   # 当没有异常的时候
        print('else')
    finally:
        # 最后一定要执行的，不管是否发生异常
        # finally 一般放置资源的清理、释放工作的语句
        print('清理工作')
        if f:
            f.close()
        # try:
        #     f.close()
        # except Exception as e:
        #     # print(e)
        #     logging.info(e)
        return     # 如果使用了break、return，表示压制异常，一般情况下不压制异常，需要处理异常
    print('=' * 30)

try:
    foo()
finally:
    print('&'*30)


# 总结：

"""
try:
    <语句>    # 运行别的代码
except <异常类>:
    <语句>    # 捕获某种类型的异常
except <异常类> as <变量名>:
    <语句>    # 捕获某种类型的异常并获得对象
else:
    <语句>    # 如果没有异常发生
finally:
    <语句>    # 退出try时总会执行
"""
