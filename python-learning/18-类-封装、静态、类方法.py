#!/usr/bin/env python
#-*- coding: utf-8 -*-

# 面向对象

# 封装

# 类属性（方法）：是类的就是大家的，所有实例共享，类属性可以使用全大写来命名

class Person:
    age = 3   # 类属性
    def __init__(self, name):
        self.name = name

    def test(self):
        print('a', self.__class__.__name__)

# Person.test() # 缺失第一参数self

# __name__
    #Person.__name__         # Prerson
    #tom.__class__.__name__  # Person


# __dict__
    #Person.__dict__   # 类字典，保存类属性
    #tom.__dict__      # 实例字典，保存实例属性：{'name': 'tom'}

# 实例属性查找顺序：
    # 实例.属性: 优先访问实例自己的属性（实例字典），如果没有，找自己类的类字典，都没有抛出AttributeError
    # tom.__dict__['weight'] dict[key] 使用key访问字典，没有key抛出KeyError

# 类属性和实例属性访问规则：
    # 1.有类时，未必有实例，使用类调用不能访问实例属性，因为不确定是哪一个实例
    # 2.反过来，通过实例可以知道（自己的）类型，可以访问类的 tom.__class__


# 类方法：@classmethod, 实例或者类方法访问方法时，会绑定 当前类，调用时注入第一参数为当前类
    # 使用场景：方法内部只需要使用类(类属性)，工具方法
class A:
    @classmethod
    def test(cls):
        print('a', type(cls), cls, cls.__name__)  # a <class 'type'> <class '__main__.A'> A


# 静态方法：@staticmethod, 剥夺了实例或类的绑定
    # 使用场景：使用极少，基本不用
class A:
    @staticmethod
    def test():    # 拿掉自动注入的参数，跟普通函数没区别
        print('a')


# 访问控制
    # public
    # peotected: _<name> 保护成员，约定，类中、子类中使用
    # private: 私有member成语，self.__<name> 包括类属性、实例属性，私有的，仅限于（当前）类中使用 _<class>.__<name> 在外部访问

class Person:
    def __init__(self, name, age=20):
        self._name = name
        self.__age = age

    def showme(self):
        return "{} is {} years old.".format(self._name, self.__age)


# property
# 把一个方法变成属性调用
class Person:
    def __init__(self, name, age):
        self._name = name
        self._aget = age

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise ValueError('Not Str!')
        self._name = value
        return self._name

    # 设置age只读
    age = property(lambda self: self._age)

# tom = Person('Tom', 18)
# tom.name = 'xiaopf'


# 封装总结：
    # 将数据和操作组织到类中，既属性和方法
    # getter, setter
    # 访问控制，保护成员或私有变量

