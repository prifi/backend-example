#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : YuLei Lan
# @Software: PyCharm


from django.http import JsonResponse
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination, CursorPagination
from rest_framework import status


class NewPageNumberPagination(PageNumberPagination):
    page_size = 10
    max_page_size = 100
    page_size_query_param = 'size'
    page_query_param = 'page'

    def get_paginated_response(self, data):
        data = {
            "code": 20000,
            "data": {
                "total": self.page.paginator.count,
                "list": data
            },
            "message": "success"
        }
        return JsonResponse(data=data, status=status.HTTP_200_OK)
