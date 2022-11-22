from django.db import models


# Create your models here.

class Employee(models.Model):
    """员工表"""
    class Gender(models.IntegerChoices):
        """如果是共用设置全局"""
        MAN = 1, '男'
        FEMALE = 2, '女'
    # 自定义主键
    emp_no = models.IntegerField(primary_key=True)
    birth_date = models.DateField()   # 默认null为false必填, blank=False
    first_name = models.CharField(max_length=14, verbose_name='姓')
    last_name = models.CharField(max_length=16, verbose_name='名')
    gender = models.SmallIntegerField(choices=Gender.choices, verbose_name='性别')
    hire_date = models.DateField()
    # salary_set 表示一关联的多端对象们

    @property
    def name(self):
        return '{} {}'.format(self.first_name, self.last_name)

    def __repr__(self):
        return '<E: {},{}>'.format(self.emp_no, self.name)

    __str__ = __repr__

    class Meta:
        verbose_name = '员工表'
        verbose_name_plural = verbose_name
        db_table = 'employees'


# 多对一
class Salary(models.Model):
    """工资表"""
    # to_field 表示关联主表哪个字段，该字段必须唯一，默认主键
    emp_no = models.ForeignKey('Employee', on_delete=models.CASCADE, db_column='emp_no', related_name='salaries')
    salary = models.IntegerField(verbose_name='工资')
    from_date = models.DateField()
    to_date = models.DateField()

    def __repr__(self):
        # 可视化打印不要打关联对象的实例，会大量查数据库, 可以查关联对象实例id, emp_no_id
        return '<S: {},{},{}>'.format(self.pk, self.emp_no_id, self.salary)

    __str__ = __repr__

    class Meta:
        verbose_name = '工资表'
        verbose_name_plural = verbose_name
        db_table = 'salaries'

# 1.从多端查，不合适，查询多次
# 2.从一端查
# xxx.__dict__.items()


# 多对多
# Many_to_Many 有多余的属性，需要建立第三张表
class Department(models.Model):
    """部门表"""
    dept_no = models.CharField(max_length=4, primary_key=True)
    dept_name = models.CharField(max_length=40, unique=True, null=False)
    # 自定义多对多关联，两边都要定义，指定中间表，查看类属性，方便引用
    # emps = models.ManyToManyField('Employee', through='Dept_emp')

    def __repr__(self):
        return '<D: {},{}>'.format(self.dept_no, self.dept_name)

    __str__ = __repr__

    class Meta:
        verbose_name = '部门表'
        verbose_name_plural = verbose_name
        db_table = 'departments'


class Dept_emp(models.Model):
    """员工-部门 中间表"""
    emp_no = models.ForeignKey('Employee', on_delete=models.CASCADE, db_column='emp_no')
    dept_no = models.ForeignKey('Department', on_delete=models.CASCADE, db_column='dept_no', max_length=4)
    # django会给外键字段自动加后缀_id，如果不需要这个后缀，使用db_cloumn指定
    from_date = models.DateField()
    to_date = models.DateField()

    def __repr__(self):
        return '<DE: {},{}>'.format(self.emp_no, self.dept_no)

    __str__ = __repr__

    class Meta:
        verbose_name = '员工部门中间表'
        verbose_name_plural = verbose_name
        db_table = 'dept_emp'
