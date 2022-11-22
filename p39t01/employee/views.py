from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

# Create your views here.
def index(request: HttpRequest, *args, **kwargs):
    print('=' * 30)
    print(request)
    print(request.method)
    print(*map(lambda x: [type(x), x], args))
    print(*map(lambda x: [x[0], type(x[1]), x[1]], kwargs.items()))  # 匹配上采用关键字传参
    print('=' * 30)
    return HttpResponse('Hello')
