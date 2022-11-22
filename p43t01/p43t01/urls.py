"""p43t01 URL Configuration

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
from rest_framework.response import Response

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# 菜单动态生成
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import api_view, permission_classes
from utils.menulist import MenuItem

'''
# 通过类构造器动态生成
 [
    {
      id: 1,
      name: '用户管理',
      children: [
        { id: 101, name: '用户列表', path: '/users/mgr' },
        { id: 102, name: '角色列表'  path: '/users/perms'}
      ]1
    },
    { id: 2, name: 'test2', children: [] }
  ]
'''


@api_view()  # GET 验证token
# @permission_classes([IsAuthenticated, IsAdminUser])  # and
@permission_classes([IsAuthenticated | IsAdminUser])  # or
def menulist_view(request):
    # print(request.user)
    # print(request.auth)
    user = request.user
    # 菜单数据哪里来？ 1.数据库(Redis) 2.写死(类构造器实现）
    menulist = []

    if user.is_superuser:  # 管理员权限才能看
        item = MenuItem(1, '用户管理')  # {'id': 1, 'name': '用户列表', 'path': None, 'children': []}
        item.append(MenuItem(101, '用户列表', '/users'))
        item.append(MenuItem(102, '角色列表', '/users/roles'))
        item.append(MenuItem(103, '权限列表', '/users/perms'))
        menulist.append(item)
    else:
        if user.has_perm('user.view_userprofile'):
            item = MenuItem(1, '用户管理')  # {'id': 1, 'name': '用户列表', 'path': None, 'children': []}
            item.append(MenuItem(101, '用户列表', '/users'))
            menulist.append(item)
        elif user.has_perm('group.view_group'):
            item = MenuItem(1, '用户管理')  # {'id': 1, 'name': '用户列表', 'path': None, 'children': []}
            item.append(MenuItem(102, '角色列表', '/users/roles'))
            menulist.append(item)
        elif user.has_perm('permissions.view_permissions'):
            item = MenuItem(1, '用户管理')  # {'id': 1, 'name': '用户列表', 'path': None, 'children': []}
            item.append(MenuItem(103, '权限列表', '/users/perms'))
            menulist.append(item)

    # CMDB Menu
    # 权限控制如何实现？
    # 1.models.py创建同名可迁移的model类,新增content_type, 生成CRUD4个默认权限
    if request.user.has_perm('cmdb.view_citype'):
        item = MenuItem(2, '资产管理')
        item.append(MenuItem(201, '资产类型', '/cmdb/citypes'))
        item.append(MenuItem(202, '资产列表', '/cmdb/cis'))
        menulist.append(item)

    # Jumpserver菜单
    item = MenuItem(3, 'JumpServer')
    item.append(MenuItem(301, '组织管理', '/jumpserver/orgs'))
    menulist.append(item)

    return Response(menulist)


tobview = TokenObtainPairView.as_view()  # 视图函数生成一次，可以多次调用

urlpatterns = [
    path('admin/', admin.site.urls),

    # APP
    # path('emp/', include('apps.employee.urls')),  # 理解Django DRF
    path('users/', include('apps.user.urls')),      # 理解认证授权，CRUD, RBAC
    # path('cmdb/', include('apps.cmdb.urls')),       # 非关系型数据库 MongoDB ODM
    path('jumpserver/', include('apps.jumpserver.urls')),       # 堡垒机，级联菜单

    # JWT认证
    path('login/', tobview, name='login'),  # 登录
    path('api/token/', tobview, name='token_obtain_pair'),  # 获取Token
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # 刷新Token（续期）

    # 菜单动态生成
    path('menulist/', menulist_view)
]
