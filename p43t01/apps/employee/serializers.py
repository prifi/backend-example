#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging

from rest_framework import serializers
from rest_framework.exceptions import ValidationError  # 自定义异常

from .models import Employee
from .models import Salary


# ModelSerializer
class SalarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Salary
        fields = "__all__"


# 重写ChoiceDisplayField，处理choice字段处理 {'gender': [ErrorDetail(string='“男” 不是合法选项。', code='invalid_choice')]}
from collections import OrderedDict
class ChoiceDisplayField(serializers.Field):
    def __init__(self, choices, **kwargs):
        self._choices = OrderedDict(choices)
        super(ChoiceDisplayField, self).__init__(**kwargs)

    def to_representation(self, obj):
        return self._choices[obj]

    def to_internal_value(self, data):
        for i in self._choices:
            if i == data or self._choices[i] == data:
                return i
        raise serializers.ValidationError("Acceptable values are {0}.".format(list(self._choices.values())))


class EmpTmpSerializer(serializers.ModelSerializer):
    # 只读字段，调用方法 get_<field_name> 返回其值
    salaries = serializers.SerializerMethodField()

    # 获取choices属性可读展示
    gender_label = serializers.CharField(source='get_gender_display', read_only=True)

    class Meta:
        model = Employee
        fields = '__all__'

    def get_salaries(self, obj):
        return [ { 'id': salary.id, 'salaries': salary.salary }  for salary in obj.salaries.all() ]


class EmpSerializer(serializers.ModelSerializer):
    # 关联字段名与model类中属性对应 **

    # 关联主键表达
    # salaries = serializers.PrimaryKeyRelatedField(many=True, read_only=True)  # 只读
    # salaries = serializers.PrimaryKeyRelatedField(queryset=Salary.objects.all(), many=True)  # 可读写

    # 关联字符串表达，使用model的__str__，写死read_only=True
    # salaries = serializers.StringRelatedField(many=True)

    # 关联对象所有字段（嵌套关系）表达
    # salaries = SalarySerializer(many=True, read_only=True)

    # 关联对象指定字段表达
    # salaries = serializers.SlugRelatedField(many=True, read_only=True, slug_field='salary')

    # 关联关系级联写入(一方写入多方)，也可以通过重写 to_internal_value() 方法写入
    # salaries = serializers.ListField(write_only=True, required=False)

    # 处理choices字段，可读
    gender = ChoiceDisplayField(choices=Employee.Gender.choices)

    class Meta:
        model = Employee  # 参照model生成字段

        # 序列化
        # fields = ["name", "create_time"]   # 三者取其一
        # exclude = ["gender"]
        fields = "__all__"
        # depth = 1

        # 反序列化
        # read_only_fields = ["first_name", ]
        extra_kwargs = {
            'first_name': {
                # 'write_only': True,
                'required': True,
                'min_length': 3,
                'max_length': 14,
                "error_messages": {
                    "required": "first_name 是必传参数.",
                    "min_length": "长度最小为3.",
                    "max_length": "长度最大为14.",
                },
            }
        }

    def save(self, **kwargs):
        """新建或更新都需要，data为当前实例，initial_data保存提交原始数据"""
        data = super().save(**kwargs)
        self.save_salaries(data, self.initial_data.pop('salaries', []))  # 一对多，一方更新多方
        data.users.set(self.initial_data.get('users', [])) # 多对多，更新对方
        return data

    @staticmethod
    def save_accounts(instance, accounts):
        queryset = instance.accounts.all()
        current_objs = []
        for i in accounts:
            try:
                obj = Salary.objects.get(pk=i)
            except Salary.DoesNotExist:
                # raise serializers.ValidationError('关联的账号不存在 ~')
                continue
            else:
                obj.provider = instance
                obj.save()
                current_objs.append(obj)
        objs = set(queryset) - set(current_objs)  # 将多对一方的关联关系置空
        if objs:
            for obj in objs:
                obj.employ_id = None
                obj.save()

    def to_representation(self, instance):
        """序列化最后一步"""
        ret = super(EmpSerializer, self).to_representation(instance)
        ret['salaries'] = [ SalarySerializer(i).data for i in instance.salaries.all()]  # 序列化关联字段
        return ret

    def to_internal_value(self, data):
        """反序列化第一步"""
        # salaries_data = data.pop('salaries')
        return super(EmpSerializer, self).to_internal_value(data)

    def get_instance(self, data):
        try:
            return Employee.objects.get(first_name=data)
        except Employee.DoesNotExist:
            return None
        except Exception as e:
            # logging.error(f"服务器内部错误: {e.args}")
            raise serializers.ValidationError(f"服务器内部错误: {e.args}")

    def create(self, validated_data):
        salary_data = validated_data.pop('salaries')
        instance = Employee.objects.create(**validated_data)
        self.save_salaries(instance, salary_data)
        return instance

    def update(self, instance, validated_data):
        salary_data = validated_data.pop('salaries')
        self.save_salaries(instance, salary_data)
        instance.save()
        return instance

    '''
    # 根据提交的id判断创建、更新、删除
    salary_data: [
        {'salary': 60117, 'from_date': '1986-06-26', 'to_date': '1987-06-26'},
        {'salary': 70117, 'from_date': '1996-06-26', 'to_date': '1997-06-26'}
    ]
    '''
    def save_salaries(self, instance, data):
        queryset = instance.salaries.all()
        current_objs = []
        for i in data:
            obj = None
            try:
                obj = Salary.objects.get(pk=i.get('id'))
                # orm 更新(没有验证)
                # obj.__dict__.update(**i)
                # obj.save()
                # 利用序列化更新
                if obj.emp_no_id != instance.emp_no:
                    raise serializers.ValidationError(f"该操作不被允许")
                i['emp_no'] = instance.emp_no
                ser = SalarySerializer(obj, data=i)
                if ser.is_valid(raise_exception=True):
                    ser.save()
            except Salary.DoesNotExist:
                # orm 新增(没有验证)
                # obj = Salary.objects.create(emp_no=instance, **i)
                # 利用序列化新增
                i['emp_no'] = instance.emp_no
                ser = SalarySerializer(data=i)
                if ser.is_valid(raise_exception=True):
                    obj = ser.save()
            except Exception as e:
                raise serializers.ValidationError(f"服务器内部错误：{e.args}")
            current_objs.append(obj)
        not_exits_objs = set(queryset) - set(current_objs)
        for obj in not_exits_objs:  # 删除不存在的对象
            obj.delete()


'''
# Serializer
# 仅用于理解序列化原理，需要重写CRUD方法
class EmpSerializer(serializers.Serializer):
    emp_no = serializers.IntegerField()
    birth_date = serializers.DateField()
    first_name = serializers.CharField(max_length=14)
    # first_name = serializers.CharField(validators=[fn,])  # 引用外部校验器（除非有复用的必要，否则不要把检验器定义在外部）
    last_name = serializers.CharField(max_length=16)
    gender = serializers.ChoiceField(choices=Employee.Gender.choices)
    hire_date = serializers.DateField()

    # 校验器测试
    # t1 = serializers.CharField(min_length=3, max_length=6, required=False, default='ab')
    # t2 = serializers.IntegerField(min_value=2, max_value=10, required=False)
    # t3 = serializers.CharField(read_only=True, default='xyz')  # 不会出现在ser.validated_data中
    # t4 = serializers.IntegerField(write_only=True, default='xyz')  # 不会出现在ser.data中
    
    # 反序列化 重写create和update
    # save() -> instance -> None -> 创建
    # save() -> instance -> not None -> 更新
    def create(self, validated_data):
        instance = Employee.objects.create(**validated_data)  # 创建
        return instance

    def update(self, instance, validated_data):
        print(instance, '更新的实例')
        print(validated_data, '更新的数据')
        # validated_date.get('emp_no') == instance.emp_no 是否等于该主键的数据
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.gender = validated_data.get('gender', instance.gender)
        # ...
        instance.save()  # 更新
        return instance

    # 反序列化 字段级验证
    def validate_first_name(self, value):
        print(type(value), value)
        if len(value) > 14:
            raise ValidationError('长度不能大于14!')
        # return 'ABC'  偷梁换柱
        return value

    # 反序列化 对象级验证(所有)，数据都在data中，例如验证传的两次密码是否一致
    def validate(self, data):
        print(data, '+++++')
        print(data.get('first_name', ''))
        # data['first_name'] = 'ABC'  偷梁换柱
        return data
'''
