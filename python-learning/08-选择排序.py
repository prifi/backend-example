#!/usr/bin/env python
#-*- coding: utf-8 -*-

# 简单选择排序，降序

nums = [1, 9, 8, 5]
nums = [9, 1, 8, 5]   # 优化，当前索引与最大值索引相同则不需要交换
nums = [9, 8, 1, 5]
length = len(nums)

def f1():
    # 索引交换
    for i in range(length - 1):  # i = 0
        maxindex = i   # i = 0
        for j in range(i+1, length): # j=1,2,3
            if nums[j] > nums[maxindex]:
                maxindex = j  # m = 1
        if i != maxindex:
            nums[i], nums[maxindex] = nums[maxindex], nums[i]
        # print(nums, i, maxindex)



# 问题：能否像冒泡排序有提前结束可能？
# [ 9, 8, 5, 1 ]
    # 答：不可以，每一趟只关心极值数的索引，依次去比较



# 选择排序优化，变种, 二元选择排序
    # 一轮排序最大值放在索引0，最小值放在 length-1
    # 比较次数， n // 2

nums = [9, 1, 8, 5]
nums = [1, 9, 8, 5]
length = len(nums)
for i in range(length // 2):  # i = 0
    maxindex = i     # mx=0
    minindex = -i-1  # mn=-1
    minorgin = minindex

    for j in range(i+1, length-i): # j=1,2,3
        if nums[j] > nums[maxindex]:
            maxindex = j  # m = 1
        if nums[minindex] > nums[-j-1]:
            minindex = -j-1

    print(maxindex, minindex)

    if i != maxindex:
        nums[i], nums[maxindex] = nums[maxindex], nums[i]  # [9, 1, 8, 5]
        # 克服交换对最小值索引的干扰
        if i == minindex or i == length + minindex:
            minindex = maxindex - length  # -3

    # 最大值与最小值相等，提前结束循环 [1,1,1,1]
    if nums[maxindex] == nums[minindex]: break

    if minorgin != minindex and nums[minindex] != nums[maxindex]:
        nums[minorgin], nums[minindex] = nums[minindex], nums[minorgin]

print(nums)
    # break




