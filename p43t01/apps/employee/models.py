from django.db import models

# Create your models here.
"""
# 员工表
Create Table: CREATE TABLE `employees` (
  `emp_no` int(11) NOT NULL,
  `birth_date` date NOT NULL,
  `first_name` varchar(14) NOT NULL,
  `last_name` varchar(16) NOT NULL,
  `gender` smallint(6) NOT NULL DEFAULT '1' COMMENT 'M=1, F=2',
  `hire_date` date NOT NULL,
  PRIMARY KEY (`emp_no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8
"""

class Employee(models.Model):
    class Gender(models.IntegerChoices):
        MAN = 1, "男"
        FEMALE = 2, "女"

    emp_no = models.IntegerField(primary_key=True, verbose_name="工号")
    birth_date = models.DateField(verbose_name="生日")
    # first_name = models.CharField(max_length=14, unique=True, db_index=True, verbose_name="名")
    first_name = models.CharField(max_length=14, null=True, blank=True, verbose_name="名")
    last_name = models.CharField(max_length=16, null=True, blank=True, verbose_name="姓")
    gender = models.SmallIntegerField(choices=Gender.choices, default=1, verbose_name="性别")
    hire_date = models.DateField(db_index=True, db_column='hire_date', verbose_name="雇佣时间")

    @property
    def name(self):
        return '{}.{}'.format(self.first_name, self.last_name)

    def __str__(self):
        return '<Emp {},{}>'.format(self.pk, self.name)

    __repr__ = __str__

    class Meta:
        db_table = 'employees'
        verbose_name = "员工表"
        verbose_name_plural = verbose_name
        unique_together = (('first_name', 'last_name'),)  # 限制，联合唯一


"""
# 工资表，与员工表多对一关系
Create Table: CREATE TABLE `salaries` (
  `emp_no` int(11) NOT NULL,
  `salary` int(11) NOT NULL,
  `from_date` date NOT NULL,
  `to_date` date NOT NULL,
  PRIMARY KEY (`emp_no`,`from_date`),  # 联合主键改id自增主键
  CONSTRAINT `salaries_ibfk_1` FOREIGN KEY (`emp_no`) REFERENCES `employees` (`emp_no`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

# 联合主键改id自增主键
ALTER TABLE `salaries` DROP FOREIGN KEY `salaries_ibfk_1`;
ALTER TABLE `salaries` DROP PRIMARY KEY; 
ALTER TABLE `salaries` ADD id int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY FIRST;
ALTER TABLE `salaries` ADD CONSTRAINT `salaries_ibfk_1` FOREIGN KEY(`emp_no`) REFERENCES employees(`emp_no`);
"""

class Salary(models.Model):
    emp_no = models.ForeignKey(
        to='Employee',
        null=True,
        blank=True,
        default=None,
        db_constraint=False,  # 不建立约束，保留关系查询
        on_delete=models.CASCADE,
        db_column='emp_no',
        related_name='salaries'
    )
    salary = models.IntegerField(verbose_name="工资")
    from_date = models.DateField(null=True, blank=True)
    to_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return '<Salary {},{}>'.format(self.emp_no, self.salary)

    __repr__ = __str__

    class Meta:
        db_table = 'salaries'
        verbose_name = "工资表"
        verbose_name_plural = verbose_name
        ordering = ('-id',)  # 倒序排序
