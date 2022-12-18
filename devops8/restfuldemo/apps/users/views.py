# 重写用户之后，调用时用get_user_model,详见源码
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission, Group
from rest_framework import viewsets, mixins, permissions, status
from rest_framework.response import Response
# from rest_framework.pagination import PageNumberPagination
from restfuldemo.pagination import Pagination

from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.authentication import TokenAuthentication, BasicAuthentication, SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from .serializers import UserSerializer, Groupserializer, PermissionSerializer
from .filters import UserFilter, GroupFilter
from .permissions import IsSuperUser

User = get_user_model()


class UsersViewset(viewsets.ModelViewSet):
    """
    create:
    创建用户
    list:
    获取用户列表
    retrieve:
    获取用户信息
    update:
    更新用户信息
    delete:
    删除用户
    """

    authentication_classes = (JSONWebTokenAuthentication, TokenAuthentication, SessionAuthentication, BasicAuthentication)
    permission_classes = (permissions.DjangoModelPermissions,)

    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = Pagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_class = UserFilter
    search_fields = ('name', 'username')
    ordering_fields = ('id',)

    def get_queryset(self):
        """
        超级管理员用户不会显示在列表中
        """
        return self.queryset.filter(is_superuser__exact=False)

    def partial_update(self, request, *args, **kwargs):
        """
        更新用户状态，局部更新
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        userobj = self.get_object()
        data = request.data
        userstatus = data.pop("is_active")
        print(userstatus)
        userobj.is_active = userstatus
        userobj.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserInfoViewset(viewsets.ViewSet):
    """
    获取当前登陆的用户信息
    """

    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication, BasicAuthentication)
    permission_classes = (permissions.IsAuthenticated,)

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def list(self, request, *args, **kwargs):
        user_obj = request.user
        roles = [role.name for role in user_obj.groups.all()]
        print(roles)
        data = {
             "name": user_obj.name,
             "roles": roles,
             "perms": request.user.get_all_permissions()
        }
        return Response(data)


class GroupsViewset(viewsets.ModelViewSet):
    """
    create:
    创建角色
    list:
    获取角色列表
    retrieve:
    获取角色信息
    update:
    更新角色信息
    delete:
    删除角色
    """
    authentication_classes = (JSONWebTokenAuthentication, TokenAuthentication, SessionAuthentication, BasicAuthentication)
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Group.objects.all()
    serializer_class = Groupserializer
    pagination_class = Pagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_class = GroupFilter
    search_fields = ('name',)
    ordering_fields = ('id',)


class PermissionsViewset(viewsets.ReadOnlyModelViewSet):
    """
    权限列表 视图类

    list:
    返回permission列表

    """
    authentication_classes = (JSONWebTokenAuthentication, TokenAuthentication, SessionAuthentication, BasicAuthentication)
    permission_classes = (permissions.IsAuthenticated, permissions.IsAdminUser)

    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    pagination_class = Pagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    search_fields = ("name", 'codename')
    ordering_fields = ('id',)


class UserGroupsViewset(mixins.UpdateModelMixin,
                        viewsets.GenericViewSet):

    """
    update:
    修改指定用户的角色
    """
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication, BasicAuthentication)
    permission_classes = (IsSuperUser,)

    queryset = User.objects.all()
    # serializer_class = UserSerializer

    # 重写update方法，只针对用户和组进行单独的处理，类似的场景还有修改密码，更改状态等
    def update(self, request, *args, **kwargs):
        user_obj = self.get_object()
        roles = request.data.get("role", [])
        print(roles)
        user_obj.groups = roles
        return Response(status=status.HTTP_204_NO_CONTENT)

    # 此处也可以通过定义serializer类，然后重写update方法实现，相比而已在view里定义更简单
    # def update(self, instance, validated_data):
    #     print(validated_data)
    #     roles = validated_data['role']
    #     instance.groups = roles
    #     return instance


class GroupsPermViewset(mixins.UpdateModelMixin,
                        viewsets.GenericViewSet):

    """
    update:
    修改指定角色的权限
    """
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication, BasicAuthentication)
    permission_classes = (permissions.IsAuthenticated,)

    queryset = Group.objects.all()
    serializer_class = Groupserializer

    def update(self, request, *args, **kwargs):
        group_obj = self.get_object()
        power = request.data.get("power", [])
        print(power)
        group_obj.permissions = power
        return Response(status=status.HTTP_204_NO_CONTENT)


class GroupMembersViewset(mixins.DestroyModelMixin,
                          viewsets.GenericViewSet):
    """
    destroy:
    从指定组里删除指定成员
    """
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication, BasicAuthentication)
    permission_classes = (IsSuperUser,)

    queryset = Group.objects.all()
    serializer_class = Groupserializer

    def destroy(self, request, *args, **kwargs):
        print(request.data)
        group_obj = self.get_object()
        uid = request.data.get('uid', 0)
        group_obj.user_set.remove(int(uid))
        return Response(status=status.HTTP_200_OK)