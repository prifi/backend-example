from django.urls import path

from .views import index

urlpatterns = [
    # path('test/<course>/<year>/', index),  # 缺省转换器 => str
    path('test/<str:course>/<int:year>/', index),  # 自定义转换器 => 指定类型
]
