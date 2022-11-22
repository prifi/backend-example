#!/usr/bin/env python
# -*- coding:utf8 -*-

# 循环

## 99乘法表
for i in range(1,10):
    for j in range(1,i+1):
        print(f'{j}*{i}={i * j}', end=' ')
    print()

for i in range(1,10):
    for j in range(1, i+1):
        print("{}*{}={:<{}}".format(j,i,i*j, 2 if j< 2 else 3), end='' if i != j else '\n')


## 用户密码验证
u = 'xiao'
p = '123'
n = 1
while True:
    u1 = input('username: >>>')
    p1 = input('password: >>>')
    if u == u1 and p == p1:
        print('Login success!!!')
        break
    else:
        print('User or Password Error, input again!!')
        n += 1
    if n > 3:
        print('fail'); break



## for 循环 else 子句
    # 循环被打破(break)不执行
for x in range(2,10):    # 4
    for y in range(2,x): # 2,3
        if x % y == 0:
            print(f'{x} = {y} * {x//y}')
            break
    else:
        print(f'------ {x} ------')

value = input('>>>: ')
print('empty' if not value else value )



## id 内存地址
a = [1,2,3]
b = [1,2,3]
print(a == b)
print(a is b)
print(id(a), id(b))

## 是否相等， == 值比较， is 内存地址比较
a = [[1]]
# b = a
b = a[::]
# b = a.copy()
# a[0][0] = 10
a[0] = 200
print(a == b)
print(a is b)
print(a, b, id(a), id(b))

a[::-1]  # 增加了内存复杂度，构建了一个垃圾副本，推荐使用 reversed(x)



## 斐波那契数列
a,b = 0,1
count = 0
print(count, b)
while True:
    count += 1
    if count > 100:
        break
    a,b = b,a+b
    print(count, b)



## 打印菱形，找共性，三元表达式
# 补空格
n = 9
e = n // 2
for i in range(-e, e+1):
    a = -i if i < 0 else i
    print(' ' * a,  '*' * (n - 2 * a), sep='')

print('-' * 10)

# 字符串居中，指定宽度 n
for i in range(-e, e+1):
    print("{:^{}}".format('*' * (n - 2 * abs(i)), n))  # '*' * (n - 2 * abs(i))


## 练习1：打印1-10内所有奇数
n2 = 0
while n2 < 10:
    n2 = n2 + 1
    if n2 % 2 == 0:
        continue
    print(n2)
print('END')
# 更好的办法利用range步长直接每隔2个取奇数
for i in range(1, 10, 2):
    print(i)


##练习2：猜数字游戏
import random
answer = random.randint(1,100)  # 生成1-100之间的随机数
count = 0
while True:
    count += 1
    # print(count)
    number = int(input('请输入一个数字：'))
    if number < answer:
        print('猜小了')
    elif number > answer:
        print('猜大了')
    else:
        print('猜对了')
        break
    if count >= 7:
        print('智商不足！')
        break
print('共猜了%d次' % count)


## 练习3：9*9乘法表
for x in range(1, 10):
    for y in range(1, x + 1):
        print('%d*%d=%d' % (x, y, x * y), end='\t')
    print()


## 练习4：输入一个正整数判断是不是素数
# 素数：只能被1和自身整除的大于1的整数
from math import sqrt
num = int(input('输入正整数：'))
is_prime = True
if num <= 0  or num == 1:
    is_prime = False
end = int(sqrt(num))
for x in range(2, end+1):
    if num % x == 0:
        is_prime = False
        break
if is_prime:
    print('%d是素数' % num)
else:
    print('%d不是素数' % num)


# 练习5：输入两个正整数计算它们的最大公约数和最小公倍数
x = int(input('输入x：'))
y = int(input('输入y：'))
if x > y:
    x, y = y, x
for factor in range(x, 0, -1):
    if x % factor == 0 and y % factor == 0:
        print('%d 和 %d 最大公约数: %d' % (x, y, factor))
        print('%d 和 %d 最小公倍数: %d' % (x, y, x * y // factor))
        break


## 练习6：打印三角形
raw=5
for i in range(raw):
    for _ in range(i + 1):
        print('*',end='')
    print()
# =======
# *
# **
# ***
# ****
# *****

for i in range(raw):   # 1
    for j in range(raw):  # 1
        # print(raw, i, j)
        if j < raw - i - 1:
            print(' ',end='')
        else:
            print('*',end='')
    print()
# ==========
#     *
#    **
#   ***
#  ****
# *****

for i in range(raw):
    for _ in range(raw - i - 1):
        print(' ', end='')
    for _ in range(2 * i + 1):
        print('*', end='')
    print()
# ==========
#     *
#    ***
#   *****
#  *******
# *********

## 扩展题： 打印菱形
#     *
#    ***
#   *****
#  *******
# *********
#  *******
#   *****
#    ***
#     *
# 伪代码
# 1 5 1
# 2 4 3
# 3 3 5
# 4 2 7
# 5 1 9
# -----
# 6 2 7
# 7 3 5
# 8 4 3
# 9 5 1
# =====
raw = 5
for i in range(raw): # 0-4
    for _ in range(raw - i): # 5-0, 5-1, 5-2, ...
        print(' ', end='')
        # print(_)
    for _ in range(2 * i + 1): # 2*0+1 1, 1*2+1 3, 2*2+1 5, 7, 9
        print('*', end='')
    print()
for j in range(raw + 1, raw * 2): # 6,10
    for _ in range(j - raw + 1):  # 6-5+1 2，7-5+1 3, 8-5+1 4, ...
        print(' ', end='')
    for _ in range(j - raw + 1, 2 * raw - (j - raw)): # 2,3,4,5 | 10-(6-5, 7-5, 8-5) 9, 8, 7, 6
        print('*', end='')
    print()



## 练习7：二分法输出数值位数（万以内）
num = int(input('num >>> '))
# 1 10 100 1000 10000
if num >= 1000:
    if num >= 10000:
        print('5位')
    else:
        print('4位')
else:
    if num >= 100:
        print('3位')
    elif num >= 10:
        print('2位')
    else:
        print('1位')


## 练习8：打印斐波那契数列 0、1、1、2、3、5、8、13、21、34 .. 100以内
a,b = 1,0
lenth = 100
while lenth:
    a,b = b,a+b  # 如果分开写需要借助临时变量
    # temp = b
    # b = a + b
    # a = temp
    print(a, end=" ")
    lenth -= 1


## 打印斐波那契数列101项
for x in range(102):
    a,b = b,a+b
    if x == 101:
        print(x,a)


## 练习9：打印100以内素数，大于1的自然数中，除了1和它本身以外不再有其他因数的数称为素数
# else子句：正常执行完循环执行else,中断则不执行
nums = 100
for num in range(2, nums):
    for i in range(2, num):
        if (num % i == 0):
            break
    else:                         # 注意 else 子句位置，否则会打印重复项
        print(num, end=' ')


## 练习10：将数字12345按位反转
num = 12345
reversed_num = 0
while num:
    reversed_num = reversed_num * 10 + num % 10  # 0+5, 50+4, 54+3, ..
    num //= 10 # 1234, 123, 12 ..
print(reversed_num)