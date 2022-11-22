#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author:flybird 2022/09/25
import operator
from functools import reduce

from django.db.models.constants import LOOKUP_SEP
from rest_framework.filters import BaseFilterBackend

from mongoengine import Q

# 自定义Mongo搜索
class MongoSearchFilter(BaseFilterBackend):
    search_param = 'search'

    def filter_queryset(self, request, queryset, view):
        search_fields = getattr(view, 'search_fields', None)  # ['name','label']
        params = request.query_params.get(self.search_param, '')  # search=???
        search_term =  params.replace('\x00', '')

        if not search_fields or not search_term:
            return queryset

        odm_lookups = [
            LOOKUP_SEP.join([str(search_field), 'icontains'])
            for search_field in search_fields
        ]  # 拼接：[label__icontains, name__icontains]

        queries = [
            Q(**{orm_lookup: search_term})
            for orm_lookup in odm_lookups
        ]  # 解构：filter(Q(label_icontains=xxx) | Q(name_icontains=xxx))
        queryset = queryset.filter(reduce(operator.or_, queries))  # 削减，两两相 or |
        # queryset = queryset.filter(reduce(operator.and_, conditions))  # and &
        return queryset
