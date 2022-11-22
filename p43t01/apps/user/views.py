from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse, Http404

from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.decorators import api_view, action


# Django 认证
# @login_required  # 失败跳转（模板）
def user_login(request):
    print(1, request.user)
    print(2, request.session)
    # if isinstance(request.user, User):
    if request.user.is_authenticated:  # 1.AnonymousUser 返回 False; 2.完成认证后下次会解析session中的user_id
        print(4, '数据库中的User实例')
    user = authenticate(username='admin', password='12345678')  # 认证完成
    print(3, user, type(user))
    # if user:
    #     login(request, user)  # 保存Sesson_data到数据库django_session表 => Token => sessionid, session_data(user_id)
    #     print(5, 'reponse阶段，中间件生成set-cookie(session)返回给浏览器')
    return HttpResponse('Login success ~')


# JWT 认证
@api_view(['GET', 'POST'])
def test_jwt_login(request: Request):
    print(1, request.COOKIES, request._request.COOKIES, request._request.headers)
    print(2, request.data)  # Json drf -> dict
    print(3, request.user, request.user.is_authenticated)  # AnonymousUser, False  # 有Token且有效
    print(4, request.auth)  # Token...
    print(5, request.META.get('HTTP_AUTHORIZATION'))  # JWT Token...
    return Response()


# User CRUD
from django.contrib.auth.models import User, Group, Permission, ContentType
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend  # 过滤
from rest_framework.filters import SearchFilter  # 搜索
from utils.exceptions import InvalidPassword  # 自定义异常
from .serializers import UserSerializer, GroupSerializer, PermSerializer


class UserViewSet(ModelViewSet):
    """用户管理"""
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    # permission_classes = [IsAdminUser]  # 管理员才能访问
    # filter_backends = [DjangoFilterBackend]
    filterset_fields = ['username', 'email']  # /?username=username 完全匹配 exact, 多个条件 and
    search_fields = ['^username', '=email']  # /?search=username # 模糊搜索 LIKE 'ad%', 多个条件 or

    # 过滤：重写, 返回字段过滤结果
    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     username = self.request.query_params.get('username', None)
    #     if username:
    #         queryset = queryset.filter(username__icontains=username)
    #     return queryset

    # 详情页禁止修改username, 剔除不需要更新的字段
    def partial_update(self, request, *args, **kwargs):
        request.data.pop('id', None)
        request.data.pop('username', None)
        request.data.pop('password', None)
        return super().partial_update(request, *args, **kwargs)

    # 禁止修改/删除id为1的管理员账户 DELETE /users/1/
    def get_object(self):
        if self.request.method.lower() != 'get':
            pk = self.kwargs.get('pk')
            if pk == 1 or pk == '1':
                raise Http404
        return super().get_object()

    # 自定义action
    @action(methods=['GET'], detail=False, url_path='whoami', permission_classes=[IsAuthenticated])  # detail=False 非详情页 /users/whoami 不带PK
    def w(self, request, **kwargs):
        return Response({
            'user': {
                'id': request.user.id,
                'username': request.user.username,
                'email': request.user.email
            }
        })

    # 重置自己密码，使用request.user已认证的用户【普通用户】
    @action(methods=['POST'], detail=False, url_path='set_self_pwd', permission_classes=[IsAuthenticated])
    def set_self_pwd(self, request):
        user = request.user
        if user.check_password(request.data.get('oldPassword', '')):
            user.set_password(request.data.get('password', ''))
            user.save()
            return Response(status=200)
        else:
            raise InvalidPassword

    # 重置别人密码，需要使用get_object获取用户对象，注意pk 【管理员权限】
    @action(methods=['POST'], detail=True, url_path='setpwd')  # detail=True 详情页 /users/100/setpwd  带PK
    def setpwd(self, request, pk=None):
        # print(request.data.get('password', ''))
        user = self.get_object()
        user.set_password(request.data.get('password', ''))
        user.save()
        return Response(status=200)

    # 获取当前用户的角色[id,]和所有角色{id,name}, /users/mgr/2/roles
    @action(methods=['GET'], detail=True, url_path='roles')
    def roles(self, request, pk=None):
        user = self.get_object()
        data = self.get_serializer(user).data
        data['roles'] = [r.get('id') for r in user.groups.values('id')]
        data['allRoles'] = Group.objects.values('id', 'name')
        return Response(data)

    # 设置当前用户的角色，与上面的GET方法对应 映射为 --> put /users/mgr/2/roles
    @roles.mapping.put
    def set_roles(self, request, pk=None):
        user = self.get_object()
        roles = request.data.get('roles', None)
        if roles is None:
            pass
        else:
            user.groups.set(roles)
        return Response(status=201)


class PermViewSet(ReadOnlyModelViewSet):
    """
    权限管理（只读）权限自动生成CRUD
    Perm格式: user.viw_userprofile
    """
    _exlude_contenttypes = [item.id for item in
                            ContentType.objects.filter(model__in=[
                                'logentry',
                                'group',
                                'permission',
                                'contenttype',
                                'session'
                            ])]  # 排除Django内建应用
    queryset = Permission.objects.exclude(content_type__in=_exlude_contenttypes)
    serializer_class = PermSerializer
    search_fields = ['^name', '^codename', ]


class GroupViewSet(ModelViewSet):
    """角色管理"""
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    search_fields = ['^name', ]

    @action(methods=['GET'], detail=True, url_path='perms')
    def perms(self, requests, pk=None):
        obj = self.get_object()
        data = self.get_serializer(obj).data  # {'id': 1, 'name': 'aaaaab', 'permissions': []} -> 当前角色权限 缺所有
        data['allPerms'] = list(PermViewSet.queryset.values('id', 'name'))
        return Response(data)


# permissions queryset.model
# print('@'*50)
# print(UserViewSet.queryset.__dict__)  # model
# print('@'*50)