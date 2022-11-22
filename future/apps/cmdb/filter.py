#!/usr/bin/env python
# encoding: utf-8
# @author: lanyulei

from django_filters import rest_framework as filters
from . import models


class ModelGroupFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = models.ModelGroup
        fields = ()
        search_fields = ('name',)


class ModelInfoFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = models.ModelInfo
        fields = ()
        search_fields = ('name',)


class FieldsFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = models.Fields
        fields = ()
        search_fields = ('name',)


class CloudAccountFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = models.CloudAccount
        fields = ()
        search_fields = ('name',)


class CloudDiscoveryFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = models.CloudDiscovery
        fields = ()
        search_fields = ('name',)
