from rest_framework import viewsets, permissions
# drf自带的分页
from rest_framework.pagination import PageNumberPagination
# drf自带的过滤器，提供了SearchFilter,OrderingFilter搜索和排序功能
from rest_framework import filters
# 第三方过滤器，高度可定制，DjangoFilterBackend 默认是精确（查找）过滤，即字段值必须要完全一样才能匹配成功
from django_filters.rest_framework import DjangoFilterBackend
# drf自带的三种用户认证方式
from rest_framework.authentication import TokenAuthentication, BasicAuthentication, SessionAuthentication
# jwt用户认证方式
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
# drf自带的权限管理方式
from rest_framework.permissions import IsAuthenticated

# 引入自定义的模型、序列化、过滤器类
from .models import Publish, Author, Book
from .serializers import PublishSerializer, AuthorSerializer, BookSerializer
from .filters import PublishFilter, AuthorFilter, BookFilter


class Pagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    page_query_param = "page"
    max_page_size = 100


class PublishViewSet(viewsets.ModelViewSet):
    """
    list:
      列出所有出版商
    retrieve:
      某个出版商的详细信息
    create:
      创建出版商
    update:
      更新出版商
    delete:
      删除出版商
    """

    # 用户认证及权限验证（四种用户模式按顺序依次匹配）
    authentication_classes = (JSONWebTokenAuthentication, TokenAuthentication, SessionAuthentication,
                              BasicAuthentication)
    permission_classes = (IsAuthenticated, permissions.DjangoModelPermissions)

    # 查询结果集
    queryset = Publish.objects.all()
    # 调用序列化类
    serializer_class = PublishSerializer
    # 调用分页类
    pagination_class = Pagination
    # 定义过滤器
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    # 调用过滤类
    filter_class = PublishFilter
    search_fields = ('name', 'city')
    ordering_fields = ('name',)


class AuthorViewSet(viewsets.ModelViewSet):
    """
    list:
      列出所有作者信息
    retrieve:
      某个作者的详细信息
    create:
      创建作者
    update:
      更新作者
    delete:
      删除作者
    """

    # 用户认证及权限验证
    authentication_classes = (JSONWebTokenAuthentication, TokenAuthentication, SessionAuthentication,
                              BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    pagination_class = Pagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_class = AuthorFilter
    search_fields = ('name', 'email')
    ordering_fields = ('name',)


class BookViewSet(viewsets.ModelViewSet):
    """
    list:
      列出所有图书信息
    retrieve:
      某个图书的详细信息
    create:
      创建图书
    update:
      更新图书
    delete:
      删除图书
    """

    # 用户认证及权限验证
    authentication_classes = (JSONWebTokenAuthentication, TokenAuthentication, SessionAuthentication,
                              BasicAuthentication)
    permission_classes = (IsAuthenticated, permissions.DjangoModelPermissions)

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    pagination_class = Pagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    # filter类和search类都可以实现模糊查询， filter的特点是可以支持区间查询，search不可以
    filter_class = BookFilter
    # 关联表道的搜索格式： 关联列名__关联表字段
    search_fields = ('name', 'publisher__name', 'authors__name')
    ordering_fields = ('publication_date',)


