#!/usr/bin/env python
#-*- coding: utf-8 -*-

# 类-反射

# 在运行时获得该对象运行信息

# __getattr__(), __setattr__(), __delattr__(), __hasattr__()
# __getattribute__()

class Point:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    # def showme(self):
    #     return "<{}:{}>".format(self.x, self.y)

t = Point(4, 5)
print(t.x, t.y)

# getattr 获取属性，可以有默认值
print(getattr(t, 'z', 30))  # 30

# setattr 设置属性，没有则创建
setattr(t, 'z', 40)
print(t.z)     # 40

# 动态设置属性或函数
# setattr(Point, 'showme', lambda self: "<{}:{}>".format(self.x, self.y))
Point.showme = lambda self: "<{}:{}>".format(self.x, self.y)

print(t.showme)
print(t.showme())

# hasattr 对象是否有属性
print(hasattr(Point, 'z'))   # False
print(hasattr(t, 'z'))       # True




# __getattr__ 当属性找不到时调用，'查找顺序：instance.__dict__ -> instance.__class__.__dict__ -> 继承的祖先类(直到Object)的__dict__,找不到时调用__getattr__()'
# __setattr__ self.x = x 或 setattr(self,'x',x)，解决方法1调用object同名方法，方法2修改自己实例字典
# __delattr__ del 实例.xxx 都会触发该魔术方法，
# __getattribute__ 属性访问第一站，一般建议不要定义，如果定义了，为了正确访问属性，建议调用object的同名方法

class Point:
    def __init__(self, x, y):
        self.x = x   # 等价：setattr(self, 'x', x)
        self.y = y

        # 批量设置实例属性
        # for k in d:
        #     self.__setattr__(k, d[k])

    def __getattr__(self, item):
        '当属性找不到时调用'
        print('getattr ~~~')
        if item == 'z':
            self.z = 100
            return self.z

    def __setattr__(self, key, value):
        '拦截对实例的属性增加，修改操作'
        print('setattr ~~~')
        # value += 10
        # super().__setattr__(key, value)  # 正确：使用父类的
        # setattr(self, key, value)        # 错误，发生递归
        self.__dict__[key] = value         # 正确：设置实例字典
        # self.a = 100                     # 错误，发生递归
        self.__dict__['a'] = 100

    def __delattr__(self, item):
        '通过实例删除属性时调用，拦截禁止删除某属性，直接删实例字典拦不住'
        print('del {} ~~~'.format(item))
        del self.__dict__[item]

t = Point(4, 5)
print(t.x)
print(t.z)  # __getattr__
print(t.a)  # __setattr__
print(t.__dict__)
del t.x     # __delattr__
print(t.__dict__)




class Point:
    def __init__(self, x, y):
        self.x = x   # 等价：setattr(self, 'x', x)
        self.y = y

    def __getattr__(self, item):
        return self.__dict__[item]

    def __getattribute__(self, item):
        print('getattrbute ~~~', item)
        # return 100
        # return getattr(self, item)   # t.x
        # return super().__getattribute__(item)   # 4
        # ret = object.__getattribute__(self, item)
        # return ret * 100   # 400
        if item != '__dict__':
            raise AttributeError
        return super().__getattribute__(item)

t = Point(4, 5)
print(t.x)       # 4


# 实例属性查找顺序：
# '__getattribute__ -> instance.__dict__ -> instance.__class__.__dict__ -> 继承的祖先类(直到Object)的__dict__,都找不到时调用__getattr__()'