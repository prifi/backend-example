#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'p43t01.settings')
django.setup(set_prefix=False)

###################################################################

from apps.employee.serializers import Employee, EmpSerializer
from apps.employee.serializers import Salary, SalarySerializer


print(EmpSerializer())  # 打印序列化器
print(SalarySerializer())

print(Employee.Gender.choices)  # 打印choice字段

# ---------------------------- 序列化 ----------------------------
# 序列化
emp = Employee.objects.get(pk=10017)
ser = EmpSerializer(emp)
print(ser.data)

emps = Employee.objects.filter(emp_no__gte=10010)
sers = EmpSerializer(emps, many=True)
print(sers.data)

print('~'*50)

# 反序列化
d = {
     'emp_no': 10044,
     'birth_date': '1958-07-06',
     'first_name': 'pengfei',
     'last_name': 'xiao',
     'gender': '男',
     'hire_date': '1993-08-03'
}

# 增
ser = EmpSerializer(data=d)
ser.is_valid(raise_exception=True)
if ser.is_valid():
     ser.save()  # 返回是创建后的instance
     print(ser.data)

# 改
emp = Employee.objects.get(pk=10033)
ser = EmpSerializer(emp, data=d)
if ser.is_valid():
     ser.save()
     print(ser.data)

# ---------------------------- 关系查询 ----------------------------
# 各自独立查询
emp = Employee.objects.get(pk='10002')
print(EmpSerializer(emp).data)  # 查员工
print(SalarySerializer(emp.salaries.all(), many=True).data)  # 查员工工资

# 关联关系级联查询
import json
data = EmpSerializer(Employee.objects.get(pk='10002')).data
print(json.dumps(data, indent=4))


# 关联关系操作，不传id为新增，传id为修改
d = {
    'emp_no': 10076,
    'birth_date': '1958-07-06',
    'first_name': 'peng fei',
    'last_name': 'xiao',
    'gender': '男',
    'hire_date': '1993-08-03',
    'salaries':[
        {'id':69, 'salary': 2, 'from_date': '1995-06-26', 'to_date': '1996-06-26'},
        {'salary': 2, 'from_date': '1995-06-26', 'to_date': '1996-06-26'},
        {'salary': 2, 'from_date': '1995-06-26', 'to_date': '1996-06-26'},
    ]
}

# 增
ser = EmpSerializer(data=d)
ser.is_valid(raise_exception=True)
print(ser.validated_data)
if ser.is_valid():
     ser.save()  # 创建后返回instance
     print(ser.data)

# 改
emp = Employee.objects.get(pk=10076)
emp_ser = EmpSerializer(emp, data=d)
print(emp_ser.is_valid(raise_exception=True))
print(emp_ser.validated_data)
emp_ser.save()
print(emp_ser.data)

# import json
# data = EmpSerializer(Employee.objects.get(pk='10061')).data
# print(json.dumps(data, indent=4))


from apps.employee.serializers import Employee, EmpTmpSerializer
# 员工查工资
emp = Employee.objects.get(pk=10001)
print(emp)
print(emp.salaries.values_list('salary', flat=True))

# 员工查工资
print(EmpTmpSerializer(emp).data)