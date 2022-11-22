#!/usr/bin/env python
# encoding: utf-8
# @author: lanyulei

from django.http import JsonResponse
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is None:
        err_message = "服务器异常错误"
    else:
        err_message = response.data
    return JsonResponse({
        "code": 40000,
        "message": err_message,
        "data": ""
    })
