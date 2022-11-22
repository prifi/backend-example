#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author:flybird 2022/07/24
from django.contrib.auth.models import User, Group, Permission, ContentType
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import UserProfile


class GroupSerializer(serializers.ModelSerializer):
    """角色序列化器"""
    name = serializers.CharField(required=True, allow_blank=False, label="角色名称", max_length=16, min_length=4,
                                     validators=[UniqueValidator(queryset=Group.objects.all(), message="角色名称必须唯一")],
                                     error_messages={
                                         "blank": "角色名称不允许为空",
                                         "required": "请输入角色名称",
                                         "max_length": "用户名长度最长为16位",
                                         "min_length": "用户名长度至少为4位"
                                     })
    class Meta:
        model = Group
        fields = '__all__'


class PermSerializer(serializers.ModelSerializer):
    """权限序列化器"""
    model = serializers.ReadOnlyField(source='content_type.model')
    app_label = serializers.ReadOnlyField(source='content_type.app_label')

    class Meta:
        model = Permission
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    """用户序列化器"""

    class Meta:
        model = UserProfile
        # fields = '__all__'
        fields = (
            'id',
            'password',
            'is_superuser',
            'username',
            'email',
            'is_active',
            'phone',
            # 'groups',
            # 'user_permissions'
        )
        extra_kwargs = {
            'username': {'max_length': 16, 'min_length': 4},
            'password': {'write_only': True},
            'is_superuser': {'default': False},
            'is_active': {'default': False}
        }

    def validate_password(self, value):
        '密码加密存储'
        # password = self.initial_data.get("password")
        if 4 < len(value) < 16:
            return make_password(value)
        raise serializers.ValidationError('The length of password must be between 4 and 16.')
