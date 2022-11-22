#!/usr/bin/env python
# encoding: utf-8
# @author: lanyulei


from django.urls import path
from . import views

urlpatterns = [
    path('model-group', views.ModelGroupViewSet.as_view({"get": "list", "post": "create"})),
    path('model-group/<int:pk>', views.ModelGroupViewSet.as_view({"put": "update", "delete": "destroy"})),

    path('model', views.ModelInfoViewSet.as_view({"get": "list", "post": "create"})),
    path('model/<int:pk>', views.ModelInfoViewSet.as_view({"put": "update", "delete": "destroy"})),

    path('fields', views.FieldsViewSet.as_view({"get": "list", "post": "create"})),
    path('fields/<int:pk>', views.FieldsViewSet.as_view({"put": "update", "delete": "destroy"})),

    path('resource', views.ResourceViewSet.as_view({"get": "list", "post": "create"})),
    path('resource/<int:pk>', views.ResourceViewSet.as_view({"put": "update", "delete": "destroy"})),

    path('resource-related', views.ResourceRelatedViewSet.as_view({"get": "list", "post": "create"})),
    path('resource-related/<int:pk>', views.ResourceRelatedViewSet.as_view({"put": "update", "delete": "destroy"})),

    path('cloud-account', views.CloudAccountViewSet.as_view({"get": "list", "post": "create"})),
    path('cloud-account/<int:pk>', views.CloudAccountViewSet.as_view({"put": "update", "delete": "destroy"})),

    path('cloud-discovery', views.CloudDiscoveryViewSet.as_view({"get": "list", "post": "create"})),
    path('cloud-discovery/<int:pk>', views.CloudDiscoveryViewSet.as_view({"put": "update", "delete": "destroy"})),
]
