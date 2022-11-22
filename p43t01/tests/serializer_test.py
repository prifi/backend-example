#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'p43t01.settings')
django.setup(set_prefix=False)

###################################################################

from apps.employee.serializers import Employee, EmpSerializer

# ---------------------------- 序列化 ----------------------------
# 1.ORM查询
emp = Employee.objects.get(pk=10010)
print(type(emp), emp)

# 2.序列化（返回给浏览器Json字符串）
# 序列化单个
ser = EmpSerializer(emp)  # 序列化器，实例 -> 字典
data = ser.data
print(type(data), data)  # dict子类 model -> 字典 -> json.dumps

# 序列化多个 many=true
emps = Employee.objects.filter(pk__gte=10017)  # Queryset
print(type(emps), emps)
sers = EmpSerializer(emps, many=True)
print(sers.data)


# ---------------------------- 反序列化 ----------------------------
# 提交数据到数据库，本质上都是使用ORM提供的CRUD方法，而不是使用序列化器操作数据库。
d = {
     'emp_no': 10030,
     'birth_date': '1963-06-01',
     'first_name': 'xiao',
     'last_name': 'pf',
     'gender': 2,
     'hire_date': '1989-08-24'
}

ser = EmpSerializer(data=d)  # 1.序列化器 json字符串 -> 字典
ser.is_valid()  # 2.校验
print(ser.is_valid())  # bool  raise_exception=True 抛出异常，不做异常压制，调试时使用
print(ser.validated_data)  # 校验后的合格数据 OrderedDict，入库使用此数据
# 3.入库
# 新增
ser.save()  # 返回新增后的实例

# 更新
instance = Employee.objects.get(pk=10030)
ser = EmpSerializer(instance, data=d)
ser.is_valid()
ser.save()  # 返回更新后的实例

# 4.返回浏览器数据
print(ser.data)  # 在save()之后调用，基于校验后的数据，给浏览器看的


# ---------------------------- 校验器 ----------------------------
# requeire为True序列化和反序列化都需要提供，默认True, 与default不能同时存在)
# require=False, default='ab' 提供默认值，缺省值不做校验
# required和read_only不能同时为True
# read_only不需要用户提供，该值提供了，反序列化也不用，仅用于序列化
# write_only序列化时不用，与read_only相反，仅用在反序列化
emp = Employee.objects.get(pk=10010)

# 序列化
# emp.t1 = 'ab'
# emp.t2 = '12'  # 序列化时校验字段类型，不校验值
# emp.t3 = 'abc'
# emp.t4 = 'def'
ser = EmpSerializer(emp)
print('序列化: ', ser.data)

# 反序列化
d = {
    'emp_no': 10010,
    'birth_date': '1963-06-01',
    'first_name': 'Duangkaew',
    'last_name': 'Piveteau',
    'gender': 2,
    'hire_date': '1989-08-24',
    # 't1': 'ab',  # 不提供使用缺省值，缺省值不做校验
    # 't2': 9,  # 反序列化时校验值和字段类型
    # 't3': 'abc',
    # 't4': '123'
}

ser = EmpSerializer(data=d)
print('反序列化: ', ser.is_valid(raise_exception=True))
print('反序列化: ', ser.data)  # 发给浏览器端的，序列化
print('反序列化: ', ser.validated_data)  # 发给后端的，入库的数据 **
