#!/usr/bin/env python
#-*- coding: utf-8 -*-

# 类-魔术方法


# __slots__
    # 限制class实例能够添加的属性
class Student:
    __slots__ = ('name', 'age')


# 类-实例化
class A:
    def __new__(cls, *args, **kwargs):   # 1.构造实例，从无到有
        print(cls)
        print(args)
        print(kwargs)
        # return 100                     # 如果返回的不是A的实例，那么实例化得到的就不是A的实例，就不会执行 __init__ 方法
        # return cls(*args)              # A(4,5) 发生递归
        # return object.__new__(cls)     # staticmethod方法，手动填入cls，返回A的实例
        return super().__new__(cls)      # 与上面等价

    def __init__(self, x, y):
        self.x = x
        self.y = y

t = A(4, 5)     # A.__new__(A)  => object.__new__(A)  => 1.A instance; 2.instance.__init__(4, 5)
print(type(t))
print(t.x)




# 类-可视化
class A:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return '{__class__.__name__} Object has attribute: {},{}'.format(self.x, self.y)

    # 对一个对象获取字符串表达，如果没有，使用基类Object的
    # [t] => [<__main__.A object at 0x7fe039335dc0>], 如何解决？ __repr__
    __repr__ = __str__

    def __bytes__(self):
        # return 'repr: {},{} ~~~'.format(self.x, self.y).encode()
        return str(self).encode()

t = A(4,5)
print(type(t))
print(t, str(t), '{}'.format(t))    # 直接调用，print, format, str 打印字符串，使用 __str__ 方法
print([t], (t,), repr(t))           # 间接调用（返回对象），使用repr返回可读字符串
print(bytes(t))                     # 返回bytes对象：b'repr: 4,5'

# 应用示例：
from pathlib import Path
p1 = Path('a/b/c')
print(p1, str(p1))    # __str__
print([p1])           # __repr__




# 类-bool
class B:
    def __bool__(self):   # 有 Bool 优先用bool, 返回bool值，没有bool使用__len__
        # return bool(0)
        return bool(len(self))

    def __len__(self):   # 容器使用长度，四大皆空，{} [] (,) set()
        return 0
        # return 1

print(bool(B))     # True
print(bool(B()))   # False
print(len(B()))    # 0




# 类-运算符重载
    # 2 > 1      class int; bool gt(int x, int y)
    # 'a' > 'b'  class str; bool gt(string x, string y)
    # Student1 > Student2  bool gt(Student x, Student y)

class Student:
    def __init__(self, name, age=20):
        self.name = name
        self.age = age

    def __gt__(self, other):   # __lt__ < > 由大于推断出小于
        print(self, other)
        # return True
        return self.age > other.age    # 返回bool值

    def __ge__(self, other):   # __le__ >= <=
        return self.age >= other.age

    def __eq__(self, other):   # __ne__ == !=
        return self.name == other.name and self.age == other.age

    def __str__(self):
        return "{}".format(self.name)

t1 = Student('tom', 30)
t2 = Student('jerry')
print(t1 > t2)          # 等价：t1.__gt__(t2)   # True
print(t1 < t2)          # 等价：t1.__gt__(t2)   # False
print(t1 >= t2)         # True
print(t2 >= t1)         # t2.__gt__(t1) # True
print(t1 == t2)         # False
t3 = Student('tom', 30)
print(t1 == t3)         # True
print(t1 is t3)         # False  内存地址比较




# 算术运算符，重载

# 实现两个学生成绩差
class Student:
    def __init__(self, name, score):
        self.name = name
        self.score = score

    def __sub__(self, other):    # 实现 - ，返回int
        other:Student = other
        print('sub ~~~')
        return self.score - other.score

    def __isub__(self, other):   # 实现就地修改 -= +=, 优先使用isub，如果没有isub使用sub
        other:Student = other
        print('isub ~~~')
        # 1. 写法一
        # self.score = self - other    # 调用sub
        # 2. 写法二
        # self.score -= other.score
        # return self
        # 3. 写法三
        return self.__class__(self.name, self - other)

    def __repr__(self):
        return "{}-{}".format(self.name, self.score)

tom = Student('tom', 90)
jerry = Student('jerry', 60)
print(tom.score - jerry.score)   # 30
print(tom - jerry)               # sub 30

tom -= jerry                     # isub， 不修改tom类型
print(type(tom), tom)            # <class '__main__.Student'> tom-30