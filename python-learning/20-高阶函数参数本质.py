#!/usr/bin/env python
#-*- coding: utf-8 -*-

# 元素小写排序
print(sorted(['a', 'Ab', '2', 'Anc'], key=lambda x: x.lower()))

def fn(x:str):
    # return x.lower()
    return str.lower(x)
# 'abc'.lower() == str.lower('abc')
# fn('abc') === str.lower('abc')  调fn相当于调str.lower, 单参函数
print(sorted(['a', 'Ab', '2', 'Anc'], key=fn))
print(sorted(['a', 'Ab', '2', 'Anc'], key=str.lower))  # 需要的是函数，不是函数调用


# 按字符串排序
print(sorted([1, 100, 12, 22], key=str))
# 等价于
def fn(x):   # 需要fn处理更加复杂的逻辑
    return str(x)
print(sorted([1, 100, 12, 22], key=fn))


# 按16进制排序
def fn(x):
    # return int(str(x), base=16)
    if isinstance(x, str):
        return int(x, 16)
    elif isinstance(x, int):
        return x
    else:
        return int(x)
print(sorted(['1', 100, 'a', '20', 7], key=fn))