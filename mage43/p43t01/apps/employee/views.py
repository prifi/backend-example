from django.http import HttpRequest, HttpResponse, JsonResponse, Http404
from django.views.decorators.http import require_GET, require_http_methods  # 视图函数装饰器
from django.views import View
from django.utils.decorators import method_decorator  # 类方法装饰器，修正第一参数self


# 视图函数装饰器(请求方法限制)，凡是视图函数装饰器都可以应用到到类或类方法上，需要修正第一参数self
# @require_http_methods(['GET', 'POST'])
# @require_GET
def test_index(request: HttpRequest, *args, **kwargs):
    # data = 'Test String'
    # return HttpResponse(data)
    print(request)
    print(request.GET)
    print(request.method.lower())
    if request.method.lower() == 'get':
        print('get')
    print(request.headers)
    data = {'name': 'xiaopf', 'age': 18}
    return JsonResponse(data)



# 3.装饰器应用到类上(总的管理)
# @method_decorator(require_GET, name='dispatch')  # 限制作用在类上
class TestView(View):
    """django.view.View类本质上就是对请求方法分发到与请求方法同步函数的调度器"""

    # 2.限制应用到分发时(总的管理)
    # 先走分发，再到handler，在该方法限制会在get,post之前
    # @method_decorator(require_GET)  # method_decorator 限制作用在方法上，使用方法装饰器修正第一参数self
    # @method_decorator(require_http_methods(['GET']))
    def dispatch(self, request, *args, **kwargs):  # 覆盖父类方法
        return super().dispatch(request, *args, **kwargs)

    # 1.限制应用在方法上(管理某一个)
    # @method_decorator(login)  # 应用场景：login是修饰视图函数的(要求必须要登录)，如果需要修饰类，需要使用method_decorator
    def get(self, request, *args, **kwargs):
        print(self.__class__.__name__, '我是视图函数，我被调用了 ~~~')
        return HttpResponse('test get request')

    def post(self, request, *args, **kwargs):
        return HttpResponse('test post request')



# Session和Cookie测试, django默认Session Engine是SeeionStore（存在数据库中）保存浏览器状态（推荐redis方案）
def test_cookie(request):
    print(request.COOKIES)  # {'ttttt': 'vvvvv', 'sessionid': 'kvxap171irf63runo3jjoz9gknz048nf'}

    # 设置一个cookie, set-cookie是response
    res = HttpResponse('t1 return')
    res.cookies['ttttt'] = 'vvvvv'  # 设置cookie，服务端不保存
    request.session['abc'] = 123  # 设置session，服务端保存，添加到sessionid相关的小字典中 {session_key:xxx, session_data:{'abc':123, ...}}
    request.session['cart'] = [1, 2, 3, 4, 5]  # 购物车商品
    cart = request.session.get('cart')
    cart.append(6)
    request.session['user_id'] = 1000  # 保存用户id
    print(request.session.items())  # dict_items([('abc', 123), ('cart', [1, 2, 3, 4, 5, 6]), ('user_id', 1000)])

    # 服务端清除session
    # print(request.session.flush())  # 清除session，删除django_session表记录
    # django中需要定时清理session
    # django-admin.py clearsessions
    # manage.py clearsessions
    return res



# DRF 视图测试
from rest_framework.views import APIView, Request, Response


class TestIndex(APIView):
    # GET 请求测试
    def get(self, request: Request):
        # print(request.user)  # User实例 未认证 AnonymousUser
        # print(request.auth)  # 未认证或者没有其他上下文 None
        print(request.method)  # request._request.method 查看原生HttpRequest属性和方法
        print(request.GET)
        print(request.query_params)  # Request属性，使用小写，多值字典，获取query_string => <QueryDict: {'a': ['1', '3'], 'b': ['2']}>
        # request.query_params.get('a', 1000)  # 单值
        # request.query_params.getlist('a')    # 多值列表
        print(request.content_type)  # text/plain
        return Response({'method': request.method, 'view': 'apiview'})

    # POST 请求测试
    def post(self, request: Request):
        print(request.method)
        print(request.query_params)  # <QueryDict: {'a': ['1', '3'], 'b': ['2']}> 获取URL中query_string（多值字典）
        print(request.POST)          # 只能拿表单数据，拿不到json方式提交数据
        print(request.data)          # 获取json提交数据（或文件），转换成字典 {"x":1, "y":"abc", "c":true, "d":null} => {'x': 1, 'y': 'abc', 'c': True, 'd': None}
        print(request.content_type)  # application/json
        return Response({'method': request.method, 'view': 'apiview'}, status=201)

    # Request 封装了django Request, 内部通过反射调用django Request属性
        # .query_params 查询参数
        # .data 提交的数据和文件，包括传统的表单提交的数据（多值字典），和json方式提交数据（字典）
    # Restponse 是django HttpResponse孙子类，覆盖增加，提供data属性将字典序列化成字符串(POST, PUT, PATCH)



# DRF CRUD CBV
from .models import Employee
from .serializers import EmpSerializer


class EmpView(APIView):
    """http://127.0.0.1:8000/emp/"""
    """http://127.0.0.1:8000/emp/10001/"""

    def get_instance(self, pk):
        try:
            ins = Employee.objects.get(pk=pk)
        except Employee.DoesNotExist:
            return Http404
        return ins

    def get(self, request, *args, **kwargs):
        if kwargs.get('pk', ''):
            # 查单条
            ins = self.get_instance(kwargs.get('pk', ''))
            if ins is None:
                return Response(status=404)
            return Response(EmpSerializer(ins).data)
        # 查全部
        emps = Employee.objects.all()
        sers = EmpSerializer(emps, many=True)
        return Response(sers.data)

    def post(self, request, *args, **kwargs):
        ser = EmpSerializer(data=request.data)
        if ser.is_valid():
            ser.save()
            return Response(ser.data, status=201)
        return Response(ser.errors, status=400)

    def put(self, request, *args, **kwargs):
        """先查后改"""
        ins = self.get_instance(kwargs.get('pk', ''))
        if ins is None:
            return Response(status=404)
        ser = EmpSerializer(ins, request.data)
        if ser.is_valid():
            ser.save()
            return Response(ser.data, status=201)
        return Response(ser.errors, status=400)

    def patch(self, request, *args, **kwargs):
        ins = self.get_instance(kwargs.get('pk', ''))
        if ins is None:
            return Response(status=404)
        ser = EmpSerializer(ins, request.data, partial=True)
        if ser.is_valid():
            ser.save()
            return Response(ser.data, status=201)
        return Response(ser.errors, status=400)

    def delete(self, request, *args, **kwargs):
        """先查后删"""
        ins = self.get_instance(kwargs.get('pk', ''))
        if ins is None:
            return Response(status=404)
        ins.delete()
        return Response(status=204)



# DRF CRUD Mixins
from rest_framework.generics import GenericAPIView, mixins
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

class EmpView(mixins.RetrieveModelMixin,
              mixins.CreateModelMixin,
              GenericAPIView):

    queryset = Employee.objects.all()
    serializer_class = EmpSerializer
    # lookup_url_kwarg = 'id'  # 覆盖默认的pk关键字，注意修改url中path定义<int:id>/

    # 重写queryset或者serializer_class，偷梁换柱
    def get_queryset(self):
        # return super().get_queryset()
        return Employee.objects.filter(pk__gte=10010)

    # def get_serializer_class(self):
    #     return super().get_serializer_class()

    # def get_object(self):
    #     obj = super().get_object()
    #     return obj

    # 重写get,post,patch..方法，等效写法
    # def get(self, request, *args, **kwargs):
    #     return self.list(request, *args, **kwargs)

    get = mixins.RetrieveModelMixin.retrieve
    post = mixins.CreateModelMixin.create
    #...



# CRUD concreate
class EmpsView(ListCreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmpSerializer

class EmpView(RetrieveUpdateDestroyAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmpSerializer



# ViewSets 视图集 路由二合一
from rest_framework.viewsets import (
    ViewSet, ViewSetMixin, GenericViewSet,
    ModelViewSet, ReadOnlyModelViewSet
)

class EmpViewSet(ModelViewSet):  # CRUD Mixin + 二合一Mixin(as_view) + GenericAPIView
    queryset = Employee.objects.all()
    serializer_class = EmpSerializer
    # lookup_url_kwarg = 'id'
