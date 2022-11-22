#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author:flybird 2022/09/27

from rest_framework.serializers import ModelSerializer

from .models import Organization, Host

class OrgSerializer(ModelSerializer):
    class Meta:
        model = Organization
        fields = '__all__'


class HostSerizlizer(ModelSerializer):
    class Meta:
        model = Host
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True},
            'ssh_pkey_path': {'write_only': True}
        }
