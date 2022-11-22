#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author:flybird 2022/09/17

from rest_framework_mongoengine import serializers
from .models import CiType, Ci


class CiTypeSerializer(serializers.DocumentSerializer):
    class Meta:
        model = CiType
        exclude = ['fields']


class CiTypeWithFieldsSerializer(serializers.DocumentSerializer):
    class Meta:
        model = CiType
        fields = '__all__'


class CiSerializer(serializers.DynamicDocumentSerializer):

    # 查看写入数据
    # def to_internal_value(self, data):
    #     print(self.initial_data)
    #     return super().to_internal_value(data)

    class Meta:
        model = Ci
        fields = '__all__'
