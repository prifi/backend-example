#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author:flybird 2022/09/17


MONGODB_DATABASES = {
    'name': 'cmdb',
    'host': '127.0.0.1',
    'port': 27017,
    # 'username': 'user',
    # 'password': 'password',
    'tz_aware': True  # 如果Django中USE_TZ = True
}


from mongoengine import connect
connect(**MONGODB_DATABASES)

from cmdb.models import CiType, CiTypeField

ct_ni = CiType()
ct_ni.name = 'Network Interface'
ct_ni.label = "网络接口"
# ct_ni.version = 1
ct_ni.fields = [
    CiTypeField(name='Interface name', label='接口名称', type='str', required=True),
    CiTypeField(name='IP Address', label='IP', type='str', required=True),
    CiTypeField(name='Mac Address', label='MAC', type='str', required=True),
    CiTypeField(name='Gateway', label='网关', type='str', required=False),
    CiTypeField(name='Net Mask', label='掩码', type='str', required=False)
]
ct_ni.save()
print(ct_ni.to_json())


print('-' * 50)


ct_server = CiType()
ct_server.name = 'Sever'
ct_server.label = '服务器'
ct_server.fields = [
    CiTypeField(name='name', label='资产名称', type='str', required=True),
    CiTypeField(name='Asset number', label='资产编号', type='str'),
    CiTypeField(name='Brand', label='品牌', type='str'),
    CiTypeField(name='Model', label='型号', type='str'),
    CiTypeField(name='OS Family', label='操作系统', type='str'),
    CiTypeField(name='OS Version', label='OS版本', type='str'),
    CiTypeField(name='Managment IP', label='管理IP', type='str'),
    CiTypeField(name='CPU', label='CPU', type='str'),
    CiTypeField(name='RAM', label='内存', type='str'),
    CiTypeField(name='Rack', label='机架', type='str'),
    CiTypeField(name='Production Date', label='上线时间', type='date'),
    CiTypeField(name='Purchase Date', label='购买日期', type='date'),
    CiTypeField(name='End of warranty', label='保修结束时间', type='date'),
    # 服务器有N个网络接口，一对多
    CiTypeField(name='Network Interface', label='网络接口', type='list:{}:{}'.format(ct_ni.name, ct_ni.version)),  # 返回最新的版本
]
ct_server.save()
print(ct_server.to_json())
