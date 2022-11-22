#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'p43t01.settings')
django.setup(set_prefix=False)

###################################################################

# 查看Session
from django.contrib.sessions.models import Session
smr = Session.objects
# print(smr.all())
session_instance = smr.get(pk='1zk8j4fmyms6ufh4a7doe0quhxaky7f1')
print(session_instance.__dict__)   # {'sessin_key':xxx, 'sessin_data':{}}
print(session_instance.expire_date)
print(session_instance.session_data)
print(session_instance.get_decoded())   # 解码：{'abc': 123, 'cart': [1, 2, 3, 4], 'user_id': 1000}