"""djangoTest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render

from django.conf import settings  # 全局配置


def index(request: HttpRequest):
    return render(request, 'index.html', {'users': [1, 2, 'a', 'b']})


def test_get(request: HttpRequest):
    """GET请求url数据在request.GET中提取"""
    print('~' * 30)
    # 查看静态搜索目录
    # print(*filter(lambda x:x[0].startswith('STATIC'), settings.__dict__.items()), sep='\n')

    # 查看GET请求
    print(request.method)
    print(request.content_type)  # text/plain
    print(request.GET)  # QueryDict, 多值字典，QueryDict 默认无法修改，可以通过 .copy() 获取可修改的副本
    # <QueryDict: {'a': ['1'], 'b': ['2', '3'], 'k1': ['1'], 'k2': ['2'], 'k3': ['3']}>
    print('~' * 30)
    response = JsonResponse({
        'book': [
            (1, 'python', 20),
            (2, 'go', 5),
        ]
    })
    # reponse.headers['Access-Control-Allow-Origin'] = 'http://127.0.0.1:8000'   # 跨域，只允许指定域名
    response.headers['Access-Control-Allow-Origin'] = '*'  # 跨域，允许所有
    return response


def test_post(request: HttpRequest):
    """POST的简单请求的数据使用request.POST提取"""
    print('-' * 30)
    print(request.method)
    print(request.content_type)  # application/x-www-form-urlencoded
    print(request.GET)  # URL -> <QueryDict: {'a': ['1'], 'b': ['2', '3']}>
    print(request.POST)  # Dict -> <QueryDict: {'p1': ['100'], 'p2': ['300']}>
    response = JsonResponse({
        'book': [
            (1, 'python', 20),
            (2, 'go', 5),
        ]
    })
    print('-' * 30)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


def test_post_json(request: HttpRequest):
    """POST的非简单请求将触发预检preflight OPTIONS请求，POST提交的数据在body中已byte形式存在"""
    print('-' * 30)
    print(request.method)
    print(request.content_type)  # application/json
    print(request.GET)  # URL -> <QueryDict: {'k1': ['v1'], 'k2': ['v2', 'v3']}>
    print(request.POST)  # {}
    print(request.body)  # json -> b'{"p1":100,"p2":300}'
    response = JsonResponse({
        'book': [
            (1, 'python', 20),
            (2, 'go', 5),
        ]
    })
    print('-' * 30)
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'content-type'
    return response


def jsonp(request: HttpRequest):
    """Jsonp只能使用GET方法"""
    # print(*filter(lambda x: x[0].lower().startswith('query'), request.META.items()), sep='\n')
    # print(*map(lambda x: x, request.META.items()), sep='\n')
    print(request.META.get('QUERY_STRING'))  # 获取query_string
    print(request.GET.get('callback'))  # 获取url提交数据
    callback = request.GET.get('callback', '')
    if callback:
        content = "{}({{a:100, b:2000}})".format(callback)  # 带数据回去
    else:
        content = {}
    return HttpResponse(content, content_type='application/javascript')


urlpatterns = [
    # 测试Ajax提交数据
    path('', index),  # / => index  获取主页
    path('testget/', test_get),  # 测试get请求
    path('testpost/', test_post),  # 测试post请求
    path('testpostjson/', test_post_json),  # 测试post提交Json请求

    # 测试jsonp
    path('jsonp/', jsonp)

    # path('admin/', admin.site.urls),
    # path('emp/', include('employee.urls'))
]
