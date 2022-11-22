from django.urls import path, include
from django.views.decorators.http import require_GET

from .views import test_index, TestView, test_cookie, TestIndex
from .views import EmpView, EmpsView
from .views import EmpViewSet

# 路由器, 与视图集配合，自动生成视图集的actions和URL
from rest_framework.routers import DefaultRouter, SimpleRouter
router = SimpleRouter()  # 创建路由器并注册我们的视图
router.register('', EmpViewSet)
"""
print(router.urls)

# 自动生成映射路径
[
<URLPattern '^$' [name='employee-list']>, 
<URLPattern '^(?P<pk>[^/.]+)/$' [name='employee-detail']>
]
"""


# 路由本质是url到视图函数的映射
urlpatterns = [
    # 视图函数
    path('index/', test_index),

    # View, 视图类
    # as_view()方法把一个类伪装成了视图函数，这个视图函数，内部使用dispatch()分发函数，
    # 内部通过反射getattr()将request.method.lower()分发给同名函数处理，找不到对应函数返回405。
    path('view/', TestView.as_view()),
    # 4.限制在url上(总的管理)，理解等价式：require_GET = require_http_methods(["GET"])(TestView.as_view())
    # path('test/', require_GET(TestView.as_view()))  # 检查限制仅允许GET请求

    # Session和Cookie
    path('cookie/', test_cookie),

    # APIView, DRF视图测试
    path('drfview/', TestIndex.as_view()),

    # 通用视图APIView, 应用CRUD
    path('', EmpsView.as_view()),  # 列表页
    path('<int:pk>/', EmpView.as_view()),  # 详情页

    # 视图集GenericViewSet, 使用viewsets需要指定对应的actions映射
    path('', EmpViewSet.as_view({
        'get': 'list',
        'post': 'create'
    })),
    path('<int:pk>/', EmpViewSet.as_view({
        'get': 'retrieve',  # list
        'put': 'update',
        'path': 'partial_update',
        'delete': 'destroy'
    })),

    # 路由器，替换actions映射，简化路由配置
    path('', include(router.urls))
]
