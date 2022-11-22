#!/usr/bin/env python
#-*- coding: utf-8 -*-

# 多进程
    # 适用于计算密集型，屏蔽了GIL带来的性能问题
    # 多进程运行必须放在 __main__ 下
    # 进程的创建消亡开销大，进程间资源隔离数据不共享
    # 数据共享方式，1.共享内存; 2.使用Queue或消息中间件(Kafka, rabbitMQ)
    # 进程间通信必须序列化、反序列化

    # 方法
        # pid
        # exitcode
        # terminate() 终止指定进程


# 多进程、多线程选择
    # CPU密集型，GIL, 多进程效率高
    # IO密集型，IO阻塞，多线程资源少

import logging
from multiprocessing import Process, Queue
from datetime import datetime

FORMAT = '%(asctime)s %(threadName)s %(message)s'
logging.basicConfig(format=FORMAT, level=logging.INFO)


# 模拟并行计算1亿个数求和，多进程方式
def task_handler(curr_list, result_queue):
    total = 0
    for number in curr_list:
        total += number
    result_queue.put(total)

def main():
    processes = []
    number_list = [x for x in range(1, 100000001)]
    result_queue = Queue()
    index = 0
    # 启动8个进程将数据切片后进行运算
    for _ in range(8):
        p = Process(target=task_handler,
                    args=(number_list[index:index + 12500000], result_queue))
        index += 12500000
        processes.append(p)
        p.start()
    # 开始记录所有进程执行完成花费的时间
    start = datetime.now()
    for p in processes:
        p.join()
    # 合并执行结果
    total = 0
    while not result_queue.empty():
        total += result_queue.get()
    print(total)
    print('Execution time: ', ((datetime.now()-start).total_seconds()), 's', sep='')

if __name__ == '__main__':
    main()

"""
# 线程安全，计算时间短：
python test.py
    5000000050000000
    Execution time: 0.815789s
"""



# concurrent.futueres包
    # 3.2版本，频繁创建线程进程代价高，异步并行编程模块，线程或进程池，复用
        # ThreadPoolExecutor
        # ProcessPoolExcutor
    # 可以拿到return返回值
    # 缺点：无法设置线程名，不重要

    # Executor子类实例方法：
        # ThreadPoolExecutor(max_workers=1)   # 池中至多创建max_workers个线程池来同时异步执行，退出时调用shutdown(wait=True)
        # submit(fn, *args, **kwargs)  # 提交执行的函数和参数，如有空闲开启daemon线程，返回Future类实例
        # shutdown(wait=True)   # 清理池，wait表示是否等待到任务线程完成

    # Future类：
        # done()         # 是否被成功的取消或执行完成，返回True
        # callcelled()   # 如果调用被成功的取消，返回True
        # running()      # 如果运行且不能被取消，返回True
        # cancel()       # 尝试取消调用，如果执行且不能被取消返回False, 否则返回True
        # result(timeout=None)    # 取返回结果

# ThreadPoolExecutor
from concurrent.futures import ThreadPoolExecutor, wait

def calc(base):
    sum = base
    for i in range(100000000):
        sum += i
    logging.info(sum)
    return sum

start = datetime.now()
with ThreadPoolExecutor(3) as executor:   # 默认shutdown阻塞
    fs = []
    for i in range(3):
        future = executor.submit(calc, i*100)
        fs.append(future)
        # results = list(executor.map(gcd, numbers))
    # wait(fs)
    print('-'*30)
for f in fs:
    print(f, f.done(), f.result())   # done不阻塞，result阻塞
print('='*30)
print((datetime.now() - start).total_seconds())


# ProcessPoolExecutor
from concurrent.futures import ProcessPoolExecutor, wait

def calc(base):
    sum = base
    for i in range(100000000):
        sum += i
    logging.info(sum)
    return sum

if __name__ == '__main__':
    start = datetime.now()
    executor = ProcessPoolExecutor(3)
    with executor:   # 默认shutdown阻塞
        fs = []
        for i in range(3):
            future = executor.submit(calc, i*100)
            fs.append(future)
        # wait(fs)
        print('-'*30)
    for f in fs:
        print(f, f.done(), f.result())   # done不阻塞，result阻塞
    print('='*30)
    print((datetime.now() - start).total_seconds())