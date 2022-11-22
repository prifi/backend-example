#!/usr/bin/env python
#-*- coding: utf-8 -*-

# 线程同步
    # 线程间协同，让一个线程访问某些数据时，其他线程不能访问这些数据，直到该线程完成对数据操作。

# Event
    # 内部标记FLag，通过true或false变化进行操作

    # 方法：
        # set()     # True
        # clear()   # False
        # is_set()  # 查看
        # wait(timeout=None)  # None表示无限等待，未等到超时返回False

from threading import Thread,Event
import logging
import time

FORMAT = '%(asctime)s %(threadName)s %(message)s'
logging.basicConfig(format=FORMAT, level=logging.INFO)

def boss(event:Event):
    logging.info("I'm boss, waiting for U")
    event.wait()   # 阻塞等待，等待flag变为True, 或者等到超时返回False
    logging.info('Good Job.')

def worker(event:Event, count=10):
    logging.info("I'm working for U")
    cups = []
    while True:
        logging.info('make 1 cup')
        time.sleep(0.5)
        cups.append(1)
        if len(cups) >= count:
            event.set()          # 通知到所有等待者，flag设置为True
            break
    logging.info('I finished my job. cups={}'.format(cups))

event = Event()
b = Thread(target=boss, name='boss', args=(event,))
w = Thread(target=worker, name='worker', args=(event,))
b.start()
w.start()

'''
def worker(event:Event, count=10):    
    logging.info("I'm working for U")
    cups = []
    while not event.wait(0.5):        #  修改上例worker中的while条件
        logging.info('make 1 cup')

        cups.append(1)
        if len(cups) >= count:
            event.set()               # 通知到所有等待者，flag设置为True
            # break
    logging.info('I finished my job. cups={}'.format(cups))
'''



# 锁
    # 多个线程对同一个资源进行写入时，线程不安全（线程加锁）；多线程读不需要加锁
    # 一旦一个线程获得锁，其他试图获取锁的线程将被阻塞，只有拥有锁的线程释放锁其他线程才有机会获取锁执行

    # 方法：
        # acquire(bloking=True, timeout=-1)  加锁，默认阻塞，阻塞可以设置超时时间，成功获取锁返回True,否则Fasle
        # release() 释放锁

    # with lock: 上下文支持，会在开始加锁，退出释放锁

    # 总结：
        # 加锁变串行，少用或不用锁
        # 加锁时间越短越好，不需要及时释放锁
        # 避免死锁

import threading
from threading import Lock
import logging
import time

FORMAT = '%(asctime)s %(threadName)s %(message)s'
logging.basicConfig(format=FORMAT, level=logging.INFO)

cups = []
lock = Lock()  # 互斥mutex

def worker(l:Lock, count=1000):
    print('work start', threading.currentThread())
    while True:
        with lock:
            # lock.acquire()      # 加锁
            if len(cups) >= count:
                # 此时如果该线程CUP时间片未执行完会重复获取锁，这里需要释放一次锁，否则会死锁！！
                # lock.release()  # 制作完成释放锁
                break
            time.sleep(0.0001)    # 制作杯子耗时
            cups.append(1)
            # lock.release()      # 制作未完成释放锁
    print('work done ==> {}'.format(len(cups)), threading.current_thread())

for i in range(10):
    threading.Thread(target=worker, name=f'w-{i}', args=(lock,), daemon=False).start()

print('-'*30)



# GIL
    # 由于GIL存在，保证内置数据类型线程安全（set,list,dict等)，读写操作原子性
        # IO密集，某个线程阻塞，GIL释放，调度其他就绪线程   -- 多线程
        # CPU计算密集，当前线程可能会连续获得GIL，导致其他线程几乎无法使用CPU  -- 多进程


# Queue
    # 适用于同一个进程内多线程安全的交换数据
    # from queue import Queue, LifoQueue
    # queue.get(), queue.put(), queue.qsize()

import queue
from queue import Queue, LifoQueue
from datetime import datetime

# 模拟计算1亿个数求和，多线程方式
def work(q:Queue, l):
    total = 0
    for n in l:
        total += n
    q.put(total)

q = Queue()
logging.info(q.qsize())   # 0
a = [i for i in range(100000001)]
c = 0
threads = []
for _ in range(5):
    t = threading.Thread(target=work, args=(q, a[c:(c+12500000)]),)
    c += 12500000

    threads.append(t)
    t.start()

start = datetime.now()
for t in threads:
    t.join()

logging.info(q.qsize())
total = 0
while not q.empty():
    total += q.get()
logging.info(total)
logging.info((datetime.now() - start).total_seconds())

"""
# 线程不安全（结果不正常），计算时间长
python t1.py
    2022-05-22 18:00:07,271 MainThread 0
    2022-05-22 18:00:17,059 MainThread 5
    2022-05-22 18:00:17,060 MainThread 1953124968750000
    2022-05-22 18:00:17,060 MainThread 2.728616
"""