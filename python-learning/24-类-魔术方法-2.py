#!/usr/bin/env python
#-*- coding: utf-8 -*-

# 类-魔术方法

# 容器化相关方法

class A(dict):               # 继承自字典拥有字典的所有方法
    # 字典或其子类使用 __getitem__() 调用时，key不存在执行该方法
    def __missing__(self, key):
        print(key)
        return 100

t = A(a=1, b='abc')
print(t, type(t), isinstance(t, dict))   # {'a': 1, 'b': 'abc'} <class '__main__.A'> True
print(t['t'])




# 应用
## 设计一个购物车，能够方便的增加商品，能够方便的遍历

class Cart:                   # 如果继承自列表以下方法都不需要写
    def __init__(self):
        self.__items = []

    def additem(self, item):
        # self.__items.append(item)
        return self + item            # 对应 __add__

    def __len__(self):
        return len(self.__items)

    def __repr__(self):
        return str(self.__items)      # "[1, 'abc', 3]"

    __str__ = __repr__

    def __iter__(self):               # 实例是可迭代对象，返回 **迭代器**
        # return iter(self.__items)
        yield from self.__items       # 同上

    def __getitem__(self, idx):       # 索引访问
        # print(idx, '+++')
        return self.__items[idx]

    def __setitem__(self, key, value): # 索引赋值
        self.__items[key]  = value

    def __add__(self, other):          # +
        if isinstance(other, list):
            self.__items.extend(other)
        else:
            self.__items.append(other)
        return self                    # 把自己返回，实现链式调用


cart = Cart()
cart.additem(1)
cart.additem('abc')
cart.additem(3)

# 长度、bool
print(cart, bool(cart), len(cart))   # __len__

print(cart)        # __repr__

# in
print(3 in cart)   # __contains__ 如果没定义，找 __iter__, 返回: True

# 索引操作
print(cart[1])     # __getitem__
cart[1] = 'xyz'    # __setitem__

# 链式编程实现加法
print(cart + 300 + 'a')    # __add__
print(cart.__add__(17).__add__(18))

# 列表 + 列表  => 扩展
print(cart + list(range(5,10)))

# 迭代
for i in cart:     # __iter__
    print(i)





# 可调用对象
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    # 将实例像函数一样调用
    def __call__(self, *args, **kwargs):
        # return "<{} {}:{}>".format(__class__.__name__, self.x, self.y)
        return repr(self)

    def __repr__(self):
        # return self()
        return "<{} {}:{}>".format(__class__.__name__, self.x, self.y)

t = Point(4,5)
print(t())
print(t)


# 累加
class Adder:
    def __call__(self, *args):
        self.result = sum(args)
        return self.result
addr = Adder()
print(addr(*range(4,7)))   # 带参数调用，等于调用 __call__ 方法
print(addr.result)




# 应用：
## 1.定义一个Fib类，方便调用，计算第n项
## 2.增加迭代数列方法、返回数列长度、支持索引查找数列项的方法，可缓存之前已经计算过的项

class Fib:
    def __init__(self):
        self.item = [0, 1, 1]

    def __str__(self):
        return str(self.item)

    __repr__ = __str__

    # def __repr__(self):
    #     return self.__str__()

    def __len__(self):
        return len(self.item)

    def __iter__(self):
        return iter(self.item)

    def __getitem__(self, index):
        if index < 0:
            raise IndexError('Index out of range')

        # if index >= len(self):   # len(self.item)   # if 可以去掉，for循环中自带判断
        for i in range(len(self), index+1):
            self.item.append(self.item[i-1] + self.item[i-2])

        return self.item[index]

    # def __call__(self, index):
    #     return self[index]       # 相当于调用：self.__getitem__(index)

    __call__ = __getitem__

f = Fib()
print(f)
print(f[5], len(f), f)    # __getitem__  # 当容器
print(f(10), len(f), f)   # __call__     # 当函数 __call__
# for x in f:
#     print(x)
print(f[5], f[6])         # 索引访问，已经算过，不需要重新计算




# __getattr__
    # 动态返回属性或函数   --掌握 重点
    # 针对完全动态的情况作调用，动态的 REST API 时很有用

class Student:
    def __init__(self):
        self._name = 'Xiaopf'

    def __getattr__(self, item):
        if item == 'score':
            # return 99         # 返回值
            return lambda : 99  # 返回函数
        if item == 'age':
            return self._age()
        # print(item, type(item))
        raise AttributeError(f'\'{__class__.__name__}\' object has no attribute \'{item}\'')   # 没找到属性时报错

    def _age(self):
        return 99

# s = Student()
# print(s.age)  # 99




# __call__
    # 直接在实例本身调用实例方法   --掌握 重点
    # instance.method('name') =>  instance('name')  可以有参数，返回可调用对象 callable(instance)

class GithubChain:
    def __init__(self, path=''):
        self._path = path

    def __getattr__(self, path):
        return self.__class__(f'{self._path}/{path}')

    def __call__(self, name):
        return self.__class__(f'{self._path}/{name}')

    def __str__(self):
        return self._path

    __repr__ = __str__


# 无论API怎么变，SDK都可以根据URL实现完全动态的调用，而且，不随API的增加而改变！
a = GithubChain().user('xiaopf').list   # => __call__('xiaopf').list => /user/xiaopf/list
b = GithubChain().user('zhangs').list   # => __call__('zhangs').list => /user/zhangs/list
print(type(a), callable(a), a)   # <class '__main__.GithubChain'> True /user/xiaopf/list
print(type(b), callable(b), b)   # <class '__main__.GithubChain'> True /user/zhangs/list



# 应用：selenium动态生成属性
'''
def __getattr__(self, loc):
    if loc not in self.locators.keys():
        raise AttributeError(f'\'{__class__.__name__}\' object has no attribute \'{item}\'')

    by, val = self.locators[loc]
    if "-" in by:
        by = get_key(by)
        return self.driver.find_elements(by, val)
    else:
        return self.driver.find_element(by, val)
'''