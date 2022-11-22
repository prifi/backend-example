from django.urls import path, include

from rest_framework.routers import SimpleRouter

from .views import user_login, test_jwt_login, UserViewSet, GroupViewSet, PermViewSet

router = SimpleRouter()
router.register('mgr', UserViewSet)
router.register('perms', PermViewSet)
router.register('roles', GroupViewSet)

urlpatterns = [
    path('login/', user_login),  # Django 认证
    path('login_jwt/', test_jwt_login),  # JWT 认证
    # path('/whoami', UserViewSet.as_view({'get':'whoami'}))  # 自定义action
    # 权限 只读
    # path('perms/', PermViewSet.as_view({'get': 'list'})),
    # path('perms/<int:pk>/', PermViewSet.as_view({'get': 'retrieve'})),
] + router.urls
