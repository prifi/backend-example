#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : YuLei Lan
# @Software: PyCharm


def jwt_response_payload(token, user=None, request=None):
    return {
        'code': 20000,
        'data': token,
        'message': "success"
    }
