#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 继承

    # 继承可以让子类从父类获取特征（属性和方法）
    # 对扩展开放，对修改封闭(OCP 开闭原则)，子类实现对基类的增强，实现多态(继承，覆盖)

# 继承中的访问控制，私有属性在继承中的特性
class Animal:
    __a = 10  # _Animal__a = 10
    _b = 20
    c = 30

    def __init__(self):
        self.__d = 40
        self._e = 50
        self.f = 60
        self.__a += 1  # self._Animal__a = self._Animal__a + 1

    def showa(self):
        print(self.__a)  # self._Animal__a 11
        print(self.__class__.__a)  # Cat._Animal__a 10

    def __showb(self):
        print(self._b)  # self._b
        print(self.__a)  # 11
        print(self.__class__.__a)  # 10


class Cat(Animal):
    __a = 100
    _b = 200


# c = Cat()
# c.showa()           # 11 10
# c._Animal__showb()  # 200 11 10
# c.c                 # 30
# c._Animal__d        # 40
# c._e                # 50
# c.f                 # 60
# c._Animal__a        # 11 # 使用实例的


# 类继承中访问控制总结：
    # 私有属性优先使用当前类的，父类的私有属性无法继承；保护属性优先使用自己的
    # 爸爸和儿子各有各的隐私


# 多态

## 覆盖(OverWrite)、锦上添花(super)

class Animal:
    def shout(self):
        print('Animal shouts')


class Cat(Animal):
    def shout(self):
        # self.__class__.__base__.shout(self)
        # Animal.shout(self)
        # super(Cat, self).shout()
        super().shout()  # 继承并发扬
        print('miao')


## 继承与初始化
class A:
    def __init__(self, a):
        self.a1 = a
        self.__d = 100

    def showme(self):
        print(self.a1, self.__d)


class B(A):
    def __init__(self, b, c):
        # A.__init__(self, b+c)
        # super(B, self).__init__(b+c) # 子类中使用父类的构造器(__init__)方法
        super().__init__(b + c)  # 借用父类的初始化构造器，创建当前子类的实例属性
        self.b1 = b
        self.b2 = c

    def showme(self):
        super().showme()    # 借用父类的方法打印私有属性
        print(self.b1, self.b2)
        print(self.a1)


c = B(1, 2)
c.showme()


# 多继承

class Document:  # 抽象基类，抽象类一般不要实例化，为了规范子类的行为
    def __init__(self, content):
        self.content = content

    def print(self):
        # 行为约束
        raise NotImplementedError("我是父类，我不实现，实现是子类做的事情")  # 父类表示子类应该实现

class World(Document): pass
class Pdf(Document): pass

class PrintableWorld(World):
    def print(self):
        print("[ {} ]".format(self.content))

class PrintablePdf(Pdf):
    def print(self):
        print("** {} **".format(self.content))

w = PrintableWorld('test world')
w.print()
p = PrintablePdf('test pdf')
p.print()



# Mixin 缺什么补什么（功能）

# 实现温度的处理        --- 理解如何设计工具类，从使用方式反推

## 华氏与摄氏温度转换
    # C = 5 * (F-32) /9
    # F = 9 * C / 5 +32
    # K = C + 273.15

# 理解为什么定义成 classmethod
class Temperature:        # 工具类的设计，提供各种工具方法

    def __init__(self, t, unit='c'):

        # 为了解决 AttributeError 提前定义
        self._c = None  # 摄氏度
        self._f = None  # 华氏度
        self._k = None  # 开氏度

        if unit == 'k':   # 无论单位 unit 传的是什么，最后都转换为摄氏度 c;
            self._k = t
            self._c = self.k2c(t)    # 体会使用classmethod好处，第一参数为类cls,可以在类内调用类方法
        elif unit == 'f':
            self._f = t
            self._c = self.f2c(t)
        else:
            self._c  = t

    @property
    def f(self):
        # print(self._f)
        if self._f is None:
            self._f = self.c2f(self._c)
        return self._f

    @property
    def k(self):
        if self._k is None:
            self._k = self.c2k(self._c)
        return self._k

    @property
    def c(self):
        return self._c

    @classmethod
    def c2f(cls, c):
        return 9 * c / 5 + 32

    @classmethod
    def f2c(cls, f):
        return 5 * (f-32) / 9

    @classmethod
    def c2k(cls, c):
        return c + 273.15

    @classmethod
    def k2c(cls, k):
        return k - 273.15

    @classmethod
    def k2f(cls, k):
        # 先从开氏度转摄氏度，再传给摄氏度转华氏度
        return cls.c2f(cls.k2c(k))

    @classmethod
    def f2k(cls, f):
        return cls.c2k(cls.f2c(f))

# print(Temperature.c2f(40))
# print(Temperature.f2c(104))
# print(Temperature.c2k(40))
# print('=' * 50)
# c = Temperature(40)
# print(c.f)
# print(c.k)
# print(c.c)



# 图形
## 有Shape基类，要求所有子类必须提供面积计算，子类有三角形，矩形，圆
## 圆类提数据可序列化

import math

class Shape:
    def __init__(self):
        self._area = None    # 保留计算结果，不重复计算属性和方法

    @property
    def area(self):
        raise NotImplementedError('基类不实现')

class Triangle(Shape):
    def __init__(self, a, b, c):
        super().__init__()
        self._a = a
        self._b = b
        self._c = c

    @property
    def area(self):
        if self._area is None:
            print('===')              # 测试打印几次
            p = (self._a + self._b + self._c) / 2
            self._area = math.sqrt(p * (p - self._a) * (p - self._b) * (p - self._c))
        return self._area

class Rectangle(Shape):
    def __init__(self, width, height):
        super().__init__()
        self.width = width
        self.height = height

    @property
    def area(self):
        if self._area is None:
            self._area = self.width * self.height
        return self._area

class Circle(Shape):
    def __init__(self, radius):
        super().__init__()
        self._r = radius

    @property
    def area(self):
        if self._area is None:
            print('===')
            self._area = math.pi * self._r * self._r
        return self._area
        # print('---')
        # return math.pi * self._r * self._r

# 序列化 Circle
import json, msgpack
class SerialzableMixin:
    def dumps(self, t='json'):
        if t == 'json':
            return json.dumps(self.__dict__)
        elif t == 'msgpack':
            return msgpack.dumps(self.__dict__)
        else:
            raise Exception

class SerializableCircle(SerialzableMixin, Circle):pass

#
# 每次创建的实例，2次
print(Triangle(3,4,5).area)
print(Triangle(3,4,5).area)
# 先创建实例后调用，1次
c = Circle(3)
print(c.area)
print(c.area)
# 使用序列化类
c1 = SerializableCircle(4)
print(c1.area)
print(c1.dumps())   # {"_area": 50.26548245743669, "_r": 4}
