#!/usr/bin/env python
# encoding: utf-8
# @author: lanyulei

from rest_framework import serializers
from rest_framework_jwt import serializers as jwt_serializers
from .models import Roles, Permissions, UserInfo


class JSONWebTokenSerializer(jwt_serializers.JSONWebTokenSerializer):
    def is_valid(self, raise_exception=None):
        return super().is_valid(raise_exception=raise_exception if raise_exception is not None else True)


class UsersSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=False)

    class Meta:
        model = UserInfo
        fields = '__all__'


class RolesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Roles
        fields = '__all__'


class PermissionsSerializer(serializers.ModelSerializer):
    title = serializers.CharField(required=True)

    class Meta:
        model = Permissions
        fields = '__all__'
