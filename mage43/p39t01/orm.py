#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoTest.settings')
django.setup(set_prefix=False)
# 以上4句固定不变

# ---------------------------------------- ORM查询 ----------------------------------------
from employee.models import Employee
emps = Employee.objects.all()


# 以下触发缓存：
[e for e in emps]  # 迭代
bool(emps)
'1001' in emps
list(emps)

print(emps._result_cache)   # 打印缓存结果
print(emps[10:15])          # 切片, 不支持负索引


# 返回查询集
mgr = Employee.objects  # all(), filter(), exclude(), order_by(), values()


# 查询集方法，支持链式查询
mgr.filter(pk=1030).exists()
mgr.filter(emp_no__gte=10015).count()
mgr.filter(first_name__contains='Kazuhito')
mgr.exclude(emp_no=10010).filter(pk=10020).values('emp_no')  # 返回字典
mgr.exclude(emp_no=10010).filter(pk=10020)
mgr.all().order_by('-emp_no')


# 返回单值
mgr.count()
mgr.exclude(emp_no=10010).first()  # first(), last(), count(), exists()查询不到返回None，有返回则True
# get返回单值，用于主键查询
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
try:
    print(mgr.get(pk=1001))    # 不存在或存在多个，报错，严格只能有一条
except (ObjectDoesNotExist, MultipleObjectsReturned) as e:
    print('no value or multi value')


# Field Lookup表达式
# exact/i, contains/i, startswitch/endswith/i, isnull/isnotnull, in, gt/e, lt/e, year, month, day, ..
mgr.filter(pk__in=[1002, 10020, 10035])

# Q对象, & | ~
# https://docs.djangoproject.com/zh-hans/3.2/topics/db/queries/#complex-lookups-with-q-objects
from django.db.models import Q
mgr.filter(pk__gte=10005).filter(pk__lte=10020)
mgr.filter(pk__gte=10005, pk__lte=10020)               # 相同功能的与关系查询，上面两个常用，后面用于复杂查询
mgr.filter(pk__gte=10005) & mgr.filter(pk__lte=10020)
mgr.filter(Q(pk__gte=10005), Q(pk__lte=10020))
mgr.filter(Q(pk__gte=10005) & Q(pk__lte=10020))

# 使用NOT 和 OR
mgr.filter(~(Q(pk__lt=10004) | Q(pk__gt=10018)))


# F对象, 将模型字段值与同一模型中的另一字段做比较
# https://docs.djangoproject.com/zh-hans/3.2/topics/db/queries/#filters-can-reference-fields-on-the-model
from django.db.models import F
mgr.filter(number_of_comments__gt=F('number_of_pingbacks'))
mgr.filter(number_of_comments__gt=F('number_of_pingbacks') * 2)  # 支持对 F() 对象进行加、减、乘、除、求余和次方
mgr.filter(authors__name=F('blog__name'))
mgr.filter(mod_date__gt=F('pub_date') + timedelta(days=3))


# group aggregate 聚合、分组
from django.db.models import Q, Count, Max, Min, Sum, Avg
mgr.filter(pk__gt=10010).count()
mgr.filter(pk__gt=10010).aggregate(Count('pk'), Max('pk'))   # 返回字典
mgr.filter(pk__gt=10010).values('gender').annotate(total=Count('gender')).order_by('-total')   # {'gender':2, 'total':7}  # 倒序


# ---------------------------------------- 关系操作 ----------------------------------------
# 多对一

# 管理器
from employee.models import Employee, Salary
emgr = Employee.objects
smgr = Salary.objects

Salary.objects.all()
print(*Employee.__dict__.items(), sep='\n')    # 查看类字典中新增关系属性 salary_set
print(*Salary.__dict__.items(), sep='\n')

# 查询10004员工所有工资
emgr.get(emp_no=10004).salary_set.all()
emgr.get(emp_no=10004).salaries.all()
emgr.get(emp_no=10004).salaries.values('emp_no', 'from_date', 'salary')  # 投影

smgr.filter(employee__pk=10004)   #　通过多查询一
Employee.objects.filter(blog__name='Beatles Blog')  # 跨关系查询
Salary.objects.filter(entry__headline__contains='Lennon')

# 查询10004员工所有工资及姓名
ret = list(smgr.filter(emp_no=10004))
for i in ret:
    print(i.emp_no.name, i.salary)   # i.emp_no会引发填充对象，会查n次数据库，用的少


# distinct 去重
# 查询所有发了工资的员工
smgr.values('emp_no').distinct()

# 工资大于55000所有员工姓名，先查出工资大于5000的去重员工工号，再在员工表in查询
emps = smgr.filter(salary__gte=55000).values('emp_no').distinct()
emgr.filter(emp_no__in=[d.get('emp_no') for d in emps])       # in操作
emgr.filter(emp_no__in=map(lambda x: x.get('emp_no'), emps))
emgr.filter(emp_no__in=emps)   # 子查询


# raw的使用（执行原生SQL）
# 工资大于55000所有员工姓名
sql = """\
select distinct e.emp_no, e.first_name, e.last_name
from employees e join salaries s
on e.emp_no=s.emp_no
where s.salary > 55000
"""
emps = emgr.raw(sql)
type(emps)
list(emps)

# 员工工资超过70000的工资和姓名
sql = """\
select e.emp_no, e.first_name, e.last_name, s.salary, e.gender
from employees e join salaries s
on e.emp_no=s.emp_no
where s.salary > 70000
"""
emps = emgr.raw(sql)
for x in emps:
    print(x.__dict__)
    print(x.gender)     # 会引发数据库n次查询，需要在查询sql中显示指定字段, e.gender


# 多对多
from employee.models import Employee, Department, Dept_emp
emgr = Employee.objects
dmgr = Department.objects

# 查看类属性
print(*Employee.__dict__.keys(), sep='\n')    # dept_emp_set
print(*Department.__dict__.keys(), sep='\n')  # dept_emp_set

# 查询10010员工所在部门编号及员工信息
emp = emgr.filter(emp_no=10010).get()
depts = emp.dept_emp_set.all()  # 懒查
for x in depts:
    print(type(x), x)   # 中间表实例
    print(x.emp_no.emp_no, x.emp_no.name, x.dept_no.dept_no, x.dept_no.dept_name)

# though
for i in dmgr.get(dept_no='d004').emps.all():
    print(i.name)