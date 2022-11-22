#!/usr/bin/env python
# encoding: utf-8
# @author: lanyulei

from rest_framework import serializers
from . import models


class ModelGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ModelGroup
        fields = '__all__'


class ModelInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ModelInfo
        fields = '__all__'


class FieldsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Fields
        fields = '__all__'


class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Resource
        fields = '__all__'


class ResourceRelatedSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ResourceRelated
        fields = '__all__'


class CloudAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CloudAccount
        fields = '__all__'


class CloudDiscoverySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CloudDiscovery
        fields = '__all__'
