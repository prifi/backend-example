# -*- coding:utf-8 -*-

"""
@author: flybird
@Created on: 2022/10/29 2:56 下午
@Description: SSH测试
"""

import paramiko


client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy) # know_hosts error

try:
    # 密码
    # client.connect('192.168.56.102', 22, 'root', '12345678')

    # 密钥
    key_filename = '/home/vagrant/.ssh/id_rsa' # 私钥
    client.connect('192.168.56.102', 22, 'root', key_filename=key_filename)

    # 返回值
    stdin, stdout, stderr = client.exec_command('id')
    print(stdout.read().decode())
except Exception as e:
    print(e)
finally:
    client.close()
