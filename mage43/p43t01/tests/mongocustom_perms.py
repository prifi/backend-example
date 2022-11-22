#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author:flybird 2022/09/18
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'p43t01.settings')
django.setup(set_prefix=False)

from django.contrib.auth.models import ContentType, Permission

# 创建自定义权限
content_type = ContentType.objects.create(app_label='cmdb', model='citype')
# 注意与默认的codename区分开，可以自动增加CRUD
# Permission.objects.create(codename='use_citype', name='Can Use 使用资产类型', content_type=content_type)
Permission.objects.create(codename='view_citype', name='Can View citype', content_type=content_type)
Permission.objects.create(codename='chanage_citype', name='Can Chanage citype', content_type=content_type)
Permission.objects.create(codename='delete_citype', name='Can Delete citype', content_type=content_type)
Permission.objects.create(codename='add_citype', name='Can Add citype', content_type=content_type)

# 测试是否包含权限
from django.contrib.auth import get_user_model
User = get_user_model()

u = User.objects.get(pk=2)
print(u)
print(u.has_perm('cmdb.change_citype'))
