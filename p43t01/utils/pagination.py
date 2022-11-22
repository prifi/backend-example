#!usr/bin/env python
# -*- coding:utf-8 -*-
from rest_framework.pagination import PageNumberPagination
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

class CustomPageNumberPagination(PageNumberPagination):
    # 设置
    page_query_param = 'page'
    page_size_query_param = "size"

    # 一页显示多少条数据
    # 默认值
    page_size = 10

    # 最大值
    max_page_size = 50

    # 自定义分页响应格式
    def get_paginated_response(self, data):
        return Response({
            'pagination': {
                'total': self.page.paginator.count,
                'size': self.page_size,
                'page': self.page.number
            },
            'results': data,
        })


class CustomLimitOffsetPagination(LimitOffsetPagination):
    # 默认显示多少条数据
    default_limit = 10
