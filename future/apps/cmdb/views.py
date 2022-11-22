from pkg.custom_model_view_set import CustomModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from . import models, serializers, filter


# 模型分组
class ModelGroupViewSet(CustomModelViewSet):
    queryset = models.ModelGroup.objects.all()
    serializer_class = serializers.ModelGroupSerializer

    filter_backends = (DjangoFilterBackend,)
    filter_class = filter.ModelGroupFilter


# 模型管理
class ModelInfoViewSet(CustomModelViewSet):
    queryset = models.ModelInfo.objects.all()
    serializer_class = serializers.ModelInfoSerializer

    filter_backends = (DjangoFilterBackend,)
    filter_class = filter.ModelInfoFilter


# 字段管理
class FieldsViewSet(CustomModelViewSet):
    queryset = models.Fields.objects.all()
    serializer_class = serializers.FieldsSerializer

    filter_backends = (DjangoFilterBackend,)
    filter_class = filter.FieldsFilter


# 资源
class ResourceViewSet(CustomModelViewSet):
    queryset = models.Resource.objects.all()
    serializer_class = serializers.ResourceSerializer


# 资源关联
class ResourceRelatedViewSet(CustomModelViewSet):
    queryset = models.ResourceRelated.objects.all()
    serializer_class = serializers.ResourceRelatedSerializer


# 云账号
class CloudAccountViewSet(CustomModelViewSet):
    queryset = models.CloudAccount.objects.all()
    serializer_class = serializers.CloudAccountSerializer

    filter_backends = (DjangoFilterBackend,)
    filter_class = filter.CloudAccountFilter


# 云账号同步
class CloudDiscoveryViewSet(CustomModelViewSet):
    queryset = models.CloudDiscovery.objects.all()
    serializer_class = serializers.CloudDiscoverySerializer

    filter_backends = (DjangoFilterBackend,)
    filter_class = filter.CloudDiscoveryFilter
