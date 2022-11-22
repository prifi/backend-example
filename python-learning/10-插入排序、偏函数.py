#!/usr/bin/env python
#-*- coding: utf-8 -*-

# 插入排序
# 核心思想：将待排序数插入到已经排好的有序区的合适位置(第一位为哨兵位)

nums = [9, 5, 8 ,1]
nums = [None] + nums  # [None, 9, 5, 8 ,1]
length = len(nums) # 5

for i in range(2, length): # i=2
    nums[0] = nums[i]   # [5, 9, 5, 8, 1]
    j = i - 1  # j=1
    if nums[j] > nums[0]:  # 减少交换次数
        while nums[j] > nums[0]:
            nums[j+1] = nums[j]  # [5, 9, 9, 8, 1]
            j -= 1  # j=0 break
        nums[j+1] = nums[0] # [5, 5, 9, 8, 1]

print(nums[1:])


# 插入排序 方法2
nums = [9, 5, 8 ,1]

for i in range(1, len(nums)):   # i=1
    key = nums[i]   # 5 [9, 5, 8, 1]

    j = i-1  # j=0
    if key < nums[j]:   # 减少交换次数
        while j >= 0 and key < nums[j]:
            nums[j+1] = nums[j]   # 5 [9, 9, 8, 1]
            j -= 1  # j = -1 break
        nums[j+1] = key  # 5 [5, 9, 8, 1]
print(nums)


# 1 1 2
# 冒泡法：稳定
# 选择排序: 不稳定
# 插入排序： 稳定



# 削减 reduce
from functools import reduce
s = reduce(lambda x,y: x+y, range(10), 100)  # 145



# 偏函数 partial
# 对一个函数部分参数固定，返回一个包装函数，新函数是关于剩余参数的一个函数
from functools import partial
def mod_2(x, y=2):
    return x % y == 0

mod_3 = partial(mod_2, y=3)
print(mod_2(4))
print(mod_3(4))


def add(x, y):
    return x + y
newadd = partial(add, y=5)
print(newadd(4))
print(newadd(4,y=5))
print(newadd(4,y=5))
# print(newadd(4,6))      # 报错 相当于传入关键字参数 {y:5}
print(newadd(y=6, x=4))


def add(x, y, *args):
    print('x:' ,x, 'y:',y, 'args', args)
    return x + y + sum(args)
newadd = partial(add, 1,2,3,4,5)
print(newadd())
print(newadd(1))          # x: 1 y: 2 args (3, 4, 5, 1)
print(newadd(1,2))
# print(newadd(x=1))      # 报错：本质上是将 偏函数传递的参数固定在了最左端
# print(newadd(x=1, y=2))

# 查看签名
import inspect
print(inspect.signature(newadd))  # (*args)
