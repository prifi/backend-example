#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author:flybird 2022/09/10
from rest_framework import exceptions
from rest_framework.permissions import DjangoModelPermissions

class CRUDModelPermissions(DjangoModelPermissions):
    perms_map = {
        'GET': ['%(app_label)s.view_%(model_name)s'],  # 增加view查看权限GET
        'POST': ['%(app_label)s.add_%(model_name)s'],
        'PUT': ['%(app_label)s.change_%(model_name)s'],
        'PATCH': ['%(app_label)s.change_%(model_name)s'],
        'DELETE': ['%(app_label)s.delete_%(model_name)s'],
    }


class CRUDDocumentPermissions(CRUDModelPermissions):
    def get_required_permissions(self, method, model_cls):
        """
        Given a model and an HTTP method, return the list of permission
        codes that the user is required to have.
        """
        # print('#'*50)
        # print(model_cls.__name__)
        # print(model_cls._meta)
        # print('#'*50)
        kwargs = {
            'app_label': model_cls._meta.get('app_label'),  # 解决：'MetaDict' object has no attribute 'app_label'
            'model_name': model_cls.__name__.lower()        # model_cls._meta.model_name
        }

        if method not in self.perms_map:
            raise exceptions.MethodNotAllowed(method)

        return [perm % kwargs for perm in self.perms_map[method]]

    def has_permission(self, request, view):
        # Workaround to ensure DjangoModelPermissions are not applied
        # to the root view when using DefaultRouter.
        if getattr(view, '_ignore_model_permissions', False):
            return True

        if not request.user or (
           not request.user.is_authenticated and self.authenticated_users_only):
            return False

        queryset = self._queryset(view)
        perms = self.get_required_permissions(request.method, queryset._document)  # 解决：'QuerySet' object has no attribute 'model'

        return request.user.has_perms(perms)

