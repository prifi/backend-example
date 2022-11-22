#!/usr/bin/evn python
#-*- coding: utf-8 -*-

# 递归函数（层级结构，不知道循环多少层）
    # 递归注意运算次数！！！

# 循环版
def fib(n):
    a = b = 1
    if n < 3:
        return 1
    for i in range(n-2):
        a, b = b, a+b
    return b

print(fib(101))


# 递归版（性能差）
def fib1(n):
    if n < 3:
        return 1
    return fib(n-1) + fib(n-2)

print(fib1(101))


# 递归版（优化版，性能次于 循环版）
def fib3(n, a=1, b=1):
    # a = b = 1
    # TODO 递归边界
    if n < 3:
        return b
    a, b = b, a+b
    return fib3(n-1, a, b )

print(fib3(101))


# 作业
#
# 1.求n阶乘  1x2x3...
## 循环
def fn0(n):
    s = 1
    for i in range(n, 1, -1):  # 5,4,3,2  # 从大到小，跳出递归的边界
        s *=i
    return s
print(fn0(5))

# 递推递归
def fn(n):
    # TODO 边界
    return 1 if n ==1 else n * fn(n-1)  # 2 * f(1)
print(fn(5))

## 尾递归优化
def fn2(n, c=1):
    return c if n == 1 else fn2(n-1, n*c)   # 每一步乘积带入
print(fn2(5))


# 2.猴子吃桃子问题
# 2 * (x+1)  # x // 2 + 1, d1 // 2 + 1
# 9 次
peach = 1
days = 9
for i in range(days):
    peach = 2 * (peach + 1)
print(peach)

# 递归版
def fn(days=9, peach=1):
    peach = 2 * (peach + 1)
    if days == 1:
        return peach
    return fn(days-1, peach)
print(fn())

# 递推公式
def peach(days):
    if days == 1:
        return 1
    return 2 * (peach(days-1) + 1)
print(peach(10))
