from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_mongoengine.viewsets import ModelViewSet

from utils.filters import MongoSearchFilter
from utils.permissions import CRUDDocumentPermissions
from .models import CiType, Ci
from .serializers import CiTypeSerializer, CiTypeWithFieldsSerializer, CiSerializer

class CiTypeViewSet(ModelViewSet):
    queryset = CiType.objects
    # queryset = CiType.objects.all()
    serializer_class = CiTypeSerializer
    permission_classes = [IsAuthenticated, CRUDDocumentPermissions]
    # permission_classes = []
    # Mongoengine CRUD权限，自己实现 ???  DRF Model => DRFM Document
    """
      File "/home/vagrant/python3venv/lib/python3.9/site-packages/rest_framework/permissions.py", line 230, in has_permission
        perms = self.get_required_permissions(request.method, queryset.model)
    AttributeError: 'QuerySet' object has no attribute 'model'
    """

    # 获取所有类型
    @action(detail=False)
    def all(self, request):
        # TODO: 该类型最后一个版本号的类型
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    # 获取指定类型的所有字段
    # 方法：
        # 1. action /cmdb/${id}/fields
        # 2. 重写 retrieve
        # 3. 不同的请求返回不同的序列化器 -- 这里使用此方式
    def get_serializer_class(self):
        # print(self.kwargs)  # {'id': '632690c278bfe58b628a1510'}
        if 'id' in self.kwargs:
            return CiTypeWithFieldsSerializer
        return super().get_serializer_class()

    # 获取带版本号的网络接口类型字段定义，/cmdb/citypes/Network Interface/1/
    @action(detail=False, url_path='(?P<name>[^/.]+)/(?P<version>[^/.]+)')  # str类型
    def get_object_by_name_and_version(self, request, name, version):
        object = self.get_queryset().get(name=name, version=version)
        serializer = CiTypeWithFieldsSerializer(object)
        return Response(serializer.data)


class CiViewSet(ModelViewSet):
    queryset = Ci.objects
    serializer_class = CiSerializer
    permission_classes = [IsAuthenticated, CRUDDocumentPermissions]
    # permission_classes = []  # 移除所有权限要求
    filter_backends = [MongoSearchFilter]
    search_fields = ['label', 'name']

# 打印权限中queryset.model定义
print('$'*50)
print(CiTypeViewSet.queryset.__dict__)  # _document
print('$'*50)