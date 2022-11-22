#!usr/bin/env python
# -*- coding:utf-8 -*-
from django.core.exceptions import PermissionDenied
from django.http import Http404
from rest_framework import exceptions, status
from rest_framework.response import Response
from rest_framework.views import exception_handler


# 自定义异常

class MagBaseException(exceptions.APIException):
    """基类定义基本异常"""
    code = 10000  # code为0表示正常，非0都是异常
    data = None
    message = "未知错误，请联系管理员"

    @classmethod
    def get_message(cls):
        return {'code': cls.code, 'data': cls.data, 'message': cls.message}


# Django DRF异常类，需要做映射和替换
class NotFound(MagBaseException):
    """自定义404异常"""
    code = 1000
    message = "找不到数据，请联系管理员"


class ValidationError(MagBaseException):
    """字段验证异常"""
    code = 1001
    message = "提交数据有误，请重新提交"

class InvalidPassword(MagBaseException):
    """密码错误"""
    code = 1002
    message = "旧密码验证错误，请重新提交"

class PermissionDenied(MagBaseException):
    """权限拒绝"""
    code = 1003
    message = "权限拒绝，请联系管理员"

# 小于100，验证错误
class InvalidUsernameOrPassword(MagBaseException):
    """JWT认证异常"""
    code = 1
    message = "用户名或密码错误"


class NotAuthenticated(MagBaseException):
    """未提供认证"""
    code = 2
    message = "未登录，请重新登录"


class InvalidToken(MagBaseException):
    """令牌过期"""
    code = 3
    message = "认证无效，请重新登录"


# code < 100 前端清除token，跳转到登录页

# 内部异常暴露细节，替换为自定义
exc_map = {
    # 'DEF异常名': MagBaseException，
    'DoesNotExist': NotFound,
    'AuthenticationFailed': InvalidUsernameOrPassword,
    'NotAuthenticated': NotAuthenticated,
    'InvalidToken': InvalidToken,
    'ValidationError': ValidationError,
    'InvalidPassword': InvalidPassword,
    'PermissionDenied': PermissionDenied
}


def custom_exception_handler(exc, context):
    """
    :param exc: 错误异常返回前端格式
    :param context: 上下文
    :return: Response object
    """
    print('*' * 50)
    print(exc)
    print(type(exc), exc.__dict__)
    print(exc.__class__.__name__)  # 根据错误类型添加异常exc_map映射
    # loging
    print('*' * 50)

    # response = exception_handler(exc, context)

    # if isinstance(exc, MagBaseException):  # 判断是什么类型的异常，如果是MagBaseException就是自定义类，直接返回消息
    # if response is not None:
    #     errmsg = exc_map.get(exc.__class__.__name__, MagBaseException).get_message()
    #     return Response(errmsg, status=200)  # 通过code判断是否成功

    # 通过异常类型找对应的异常类处理
    errmsg = exc_map.get(exc.__class__.__name__, MagBaseException).get_message()
    return Response(errmsg, status=200)
