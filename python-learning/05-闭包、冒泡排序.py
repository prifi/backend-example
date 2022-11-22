#!/usr/bin/env python
#-*- coding:utf-8 -*-

# 闭包，匿名函数，生成器函数，冒泡排序


## 闭包
# 内部函数引用外部函数自由变量

## 函数执行原理：
    # 执行时创建局部变量，执行完成局部变量消亡。 a,x,inner

def inc():
    a = 1
    x = [0]  # 自由变量
    print(hash(id(x)))
    def inner():
        x[0] += 1   # 没有对 x 重新赋值，仅改变 x 中的元素，执行到此处，发生闭包，使用 __closure__ 执行外部变量x地址
        # a = 123
        print(a)
        return x[0]
    return inner

foo = inc()
print(foo.__name__, type(foo.__name__))
print(foo.__closure__)
print(1, foo())
print(2, foo())


## global 声明为外部也可以用的全局变量
def counter():
    global count   # 此处也需要声明，否则将使用到局部变量 count
    count = 0
    def inc():
        global count
        count += 1
        return count
    return inc
foo = counter()
print(foo())  # 1
# count=100  # 影响结果
print(foo())  # 2


## nonlocal 变量标记不在本地定义，使用 上一层作用域（函数）局部 作用域变量，不能是全局变量
def fn():
    c = 0
    def inc():
        nonlocal c
        c += 1   # 使用到了闭包
        return c
    return inc

foo = fn()
c = 100  # 不影响结果
print(foo(), foo())



## 匿名函数 lambda
print((lambda :0)())

# 带缺省值, keyword-only
print((lambda x, *, y=5: x * 10 + y)(2,y=3))

# 可变参数
print((lambda *args: [x+1 for x in args])(*range(5)))

# 构建字典带默认列表
print({ x:[100] for x in 'abcde' })

# map、lambda 结合
d = dict(map(lambda x:(str(x), x+1), range(5)))
print(d)

# 产生字典序列带默认值
d1 = { str(i):i+1 for i in range(5) }
print(d1)

# defaultdict
from collections import defaultdict
# d3 = defaultdict(list)
# d3 = defaultdict(lambda : list())
d3 = defaultdict(lambda : [100])  # 默认带 [100]
d3['a'].append(10)
print(d3)

# sorted
x = ['a', 1, 'b', 2, 'c', 3]
print(sorted(x, key=str))

# 按数字排序
def foo(x):
    return x if isinstance(x, int) else int(x, 16)
print(sorted(x, key=foo))

print(sorted(x,key=lambda x: x if isinstance(x, int) else int(x, 16)))



## 生成器函数
    # ()
    # yield
def g():
    c = 1
    while c < 5:
        c += 1
        yield c  # 遇到yield返回
print(g, type(g))
a = g()
print('---', next(a))
print('---', next(a))
print('---', next(a))
print('---', next(a))
# print('---', next(a))  # StopIteration
# for i in a:      # 使用迭代的方式
#     print(i, '---')

def foo():
    print(1)
    yield 2
    print(3)
    yield 4
    print(5)
    return 6  # return值拿不到，可使用异常捕获 StopIterator
    # yield 7  # retuen 后的 yield 不会返回
x = foo()
for i in foo():
    print(i, '---', end=' ')
# print(next(x))
# print(next(x))
# print(next(x))


## 生成器应用：

# 1.无限容器
def foo():
    count = 0
    while True:
        count += 1
        yield count


# 2.计数器
def inc():
    def foo():
        count = 0
        while True:
            count += 1
            yield count
    c = foo()   # 返回生成器对象
    # def fn():
    #     return next(c)   # 使用到了闭包，可使用lambda函数实现
    return lambda : next(c)
    # return c
    # return fn
a = inc()
# print(next(a), '===')
print(a, type(a), a.__name__)
print(a(), '===')  # 好处不需要写next()
print(a(), '===')


## 捕获 yield 最后的 return 值
def a():
    yield 1
    yield 2
    print(5)
    return 6
f = a()
print(next(f))
print(next(f))
try:
    print(next(f))
except StopIteration as e:   # 捕获Return值
    print('Return:>', e.value)


## 斐波那契数列，生成器函数版本
def fib(c):
    n, a, b = 0, 0, 1
    while n < c:
        yield b
        a, b = b, a+b
        n += 1
    return 'done'
# g = fib(6)
# for i in g:  # 迭代方式
#     print(i, end=' ')
g = fib(6)
while True:
    try:
        print(next(g), end=' ')
    except StopIteration as e:
        print(e.value)      # 拿到 return 值
        break

# 杨辉三角
def triiangles():
    L = [1]
    while True:
        yield L
        # print(len(L))
        L = [1] + [ L[n] + L[n+1] for n in range(len(L)-1) ] + [1]

results = []
g = triiangles()
for _ in range(10):
    results.append(next(g))

for t in results:
    print(t)



# yield from
# 从 from 后面的 可迭代对象 中拿元素一个个 yield 出去
def inc():
    for x in range(10):
        yield x + 10
def inc1():
    # yield from range(10)
    yield from map((lambda x: x + 10), range(10))  # lamba 执行更加复杂的逻辑
# 相等
a = inc()
a1 = inc1()
for i in a:
    print(i, end=' ')
print()
for j in a1:
    print(j, end=' ')
print()


## 作业：编写函数，实现内建函数map功能
    # map 将一个函数依次作用在一个可迭代对象中的元素，返回生成器对象
def mymap(func, iterable, /):
    # print(func)
    # print(iterable)
    def foo():
        for i in iterable:
            yield func(i)
    c = foo()
    return c
a = mymap(str, [1,2,3])
print(a, type(a))
print(list(mymap(str, [1,2,3])))
print("".join(mymap(str, [1,2,3])))



## 冒泡排序（升序）
    # 时间复杂度 O(n**2)
    # 无序列表减小，有序列表增大
nums = [0, 1, 2, 4, 3]  # 比较次数：4，3，2，1 | 4, 3(如果后面未发生交换，提前中断)
c = 0
s = 0
for i in range(len(nums)-1): # 0 1 2 # 控制趟数，4个数比3下，每一趟产生 1 个有序数字
    swap = False   # 假设不需要进行交换，说明已经是有序队列，提前中断比较，减少比较次数（优化冒泡排序）
    for j in range(len(nums) - 1 - i): # 0 1 2  # 控制比较次数，减去每趟产生的有序列表大小 i
        c += 1
        if nums[j] > nums[j+1]:
           nums[j], nums[j+1] = nums[j+1], nums[j]   # 交换
           swap = True
           s += 1
    if not swap: break  # 如果已经是有序的，提前跳出循环
print(nums)
print(c, s)