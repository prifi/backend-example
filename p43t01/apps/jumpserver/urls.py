#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author:flybird 2022/09/27

from django.urls import path

from rest_framework.routers import SimpleRouter

from .views import OrgViewSet, HostViewSet, upload

router = SimpleRouter()
router.register('orgs', OrgViewSet)
router.register('hosts', HostViewSet)

urlpatterns = [
    path('upload/', upload)
] + router.urls
