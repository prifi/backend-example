#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 中间件: https://docs.djangoproject.com/en/3.2/topics/http/middleware

from django.http import HttpResponse, HttpRequest


class MagMiddleware1:
    def __init__(self, get_response):
        # 启动时执行一次初始化，注意配置中间件的顺序，实例化顺序相反
        print(self.__class__.__name__, "init ~~~~~ settings配置中自下而上load_middlewares")
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request: HttpRequest):
        # 实例是可调用实体，每个请求都是该实例的独立调用
        # process_request
        # 在到达视图函数之前执行，可以拦截request，做请求的拦截处理，例如：限制某个IP请求 ('REMOTE_ADDR', '10.0.2.2')
        print(*filter(lambda x: x[0] == 'REMOTE_ADDR', request.META.items()), sep='\n')
        print(self.__class__.__name__, "process_request 执行前 ~~~~~ 由外向内依次调用process_request")
        response = self.get_response(request)  # 等待后面的 中间件M2 或者 视图函数 返回响应
        # process_response
        # 返回浏览器，可以拦截request和response
        print(self.__class__.__name__, "process_response 执行后 ~~~~~ 由内向外依次return process_response")
        # return HttpResponse('M1 process response return', status=201)   # 覆盖preview的返回值，直接响应给浏览器端
        return response

    def process_view(self, request: HttpRequest, view_func, view_args, view_kwargs):
        """
        调用视图前被调用，返回值是None或HttpResponse对象
        https://docs.djangoproject.com/en/3.2/topics/http/middleware/#process-view
        """
        # 这个钩子里面才能用view函数 -> view_func -> TestView.as_view()
        print(self.__class__.__name__, "prcess_view~~~~", view_func.__name__, view_args, view_kwargs)
        # return None 继续向后执行
        # return HttpResponse(self.__class__.__name__ + ' process_view')  # 不再执行其他函数的preview，此函数返回值作为浏览器端响应
        # 还需要执行M2的process_response,穿透多深返回多深


class MagMiddleware2:
    def __init__(self, get_response):
        print(self.__class__.__name__, "init ~~~~~ 配置中自下而上load_middlewares")
        self.get_response = get_response

    def __call__(self, request):
        print(self.__class__.__name__, "process_request 执行前 ~~~~~ 由外向内依次调用process_request")
        response = self.get_response(request)  # 等待后面的 中间件 或者 视图函数view 返回响应
        print(self.__class__.__name__, "process_response 执行后 ~~~~~ 由内向外依次return process_response")
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        print(self.__class__.__name__, "prcess_view~~~~", view_func.__name__, view_args, view_kwargs)
        # return HttpResponse(self.__class__.__name__ + ' process_view')
