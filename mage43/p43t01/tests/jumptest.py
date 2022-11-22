#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author:flybird 2022/10/17
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'p43t01.settings')
django.setup(set_prefix=False)

from apps.jumpserver.serializers import Organization, OrgSerializer


# ---- 组织树 增加节点 ----
# obj = Organization.objects.get(id=1, name='北京')
# Organization.objects.create(name='昌平',parent=obj)
# Organization.objects.create(name='回龙观',parent=obj)
# obj = Organization.objects.get(name='深圳')
# obj1 = Organization.objects.get(name='龙岗')
# Organization.objects.create(name='坂田',parent=obj1)
# Organization.objects.create(name='南京')

'''
querset = Organization.objects.all()
results = []
nodemap = {}
for o in querset:
    pid = o.parent_id
    id = o.id
    data = OrgSerializer(o).data
    data.setdefault('children', [])
    nodemap[id] = data
    if pid:
        nodemap[pid]['children'].append(data)
    else:
        results.append(data)

print(results)
'''

# ---- 组织树 删除节点 ----
pk = None  # null 祖先节点 pk=null
# pk = 1
if pk:
    targets = [pk] # 需要删除的节点id，不包括 null
pids = [pk] # 父节点

while pids:
    # 子节点ids
    if pids[0] is None:
        cids = Organization.objects.filter(parent = None).values_list('id', flat=True)
    else:
        cids = Organization.objects.filter(parent__in=pids).values_list('id', flat=True)
    targets.extend(cids)
    pids = cids  # 递归查子ids

print(pids)
print(targets)
