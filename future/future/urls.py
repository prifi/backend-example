"""future URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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

from django.urls import path, include
from .settings.base import API_VERSION
from rest_framework.documentation import include_docs_urls
from apps.system.views import ObtainJSONWebToken
from apps.system import urls as system_urls
from apps.cmdb import urls as cmdb_urls

urlpatterns = [
    # api文档
    path(f'{API_VERSION}/docs', include_docs_urls(title="future 接口文档", permission_classes=[])),

    # 登陆验证
    path(f'{API_VERSION}/login', ObtainJSONWebToken.as_view()),

    # system
    path(f'{API_VERSION}/system/', include(system_urls)),

    # cmdb
    path(f'{API_VERSION}/cmdb/', include(cmdb_urls)),
]
