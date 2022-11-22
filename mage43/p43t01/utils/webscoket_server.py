# -*- coding:utf-8 -*-

"""
@author: flybird
@Created on: 2022/10/30 4:24 下午
@Description: WebSocket Server 监听 10800
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'p43t01.settings')
django.setup(set_prefix=False)
### 以上4句固定

# system
import json
import asyncio
import websockets
import paramiko
from asgiref.sync import sync_to_async

# third
from websockets.legacy.server import WebSocketServerProtocol

# drf
from rest_framework_simplejwt.authentication import JWTAuthentication

# apps
from apps.jumpserver.models import Host, Track
from django.conf import settings

# 同步变异步
# @sync_to_async  # get_user = sync_to_async(get_user), 函数签名需要一样
# def get_user(jwtauth, valiadated_token):
#     return jwtauth.get_user(valiadated_token)

@sync_to_async
def get_host(id):
    return Host.objects.filter(is_delete=False).get(pk=id)

@sync_to_async
def log(user, host, source_ip, op_type, command=None, op_state=True):
    return Track.objects.create(
        user=user, host=host, source_ip=source_ip, op_type=op_type, op_state=op_state, command=command
    )

async def handler(websocket: WebSocketServerProtocol, path):
    print(type(websocket), websocket) # socket对象
    print(type(path), path) # url path路径路由不同函数 ws://127.0.0.1:10800/webshell -> /webshell
    print('-'*50)

    try:
        # 第一次接收浏览器发来数据, 接收并验证Token, 获取User对象，判断权限
        first_data = await websocket.recv()
        payload = json.loads(first_data)
        raw_token = payload['token']

        # 拿到token, 如何验证? JWT验证token
        jwtauth = JWTAuthentication()
        valiadated_token = jwtauth.get_validated_token(raw_token)

        # user = jwtauth.get_user(valiadated_token) # 同步，查数据库 user_id
        # 报错：同步变异步 get_user()
        # user = await get_user(jwtauth, valiadated_token) # 装饰器方式
        user = await sync_to_async(jwtauth.get_user)(valiadated_token) # 柯里化
        print(type(user), user)

        # 如果验证不通过，报错
        # if True:
        #     await websocket.close(reason="认证失败")

        # TODO user与命令组、命令之间 关系 禁止高危命令
        # TODO 权限验证，略 user.has_prems()

        # 获取主机信息，密码或密钥
        host_id = payload['hostId']
        host = await get_host(host_id)
        ip = host.ip
        username = host.username
        password = host.password

        # parmiko ssh 连接
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        if password: # paramiko
            client.connect(ip, 22, username, password)  # 密码访问
        else:
            pkey_filename = str(settings.JUMPSERVER_UPLOAD_BASE / host.ssh_pkey_path)
            client.connect(ip, 22, username, key_filename=pkey_filename) # 密钥访问

        # 登录记录 审计
        sip = websocket.remote_address
        await log(user, host, sip, Track.OPTYPES.LOGIN)

        # 第二次接收浏览器发来的命令
        with client:
            while True:
                data = await websocket.recv()
                # TODO 特殊字符退出
                if data == 'exit':
                    await websocket.close()
                    # 登出记录 审计
                    await log(user, host, sip, Track.OPTYPES.LOGOUT)
                # TODO 利用client执行命令返回结果，发给浏览器
                _, stdout, stderr = client.exec_command(data)
                # 操作记录 审计
                await log(user, host, sip, Track.OPTYPES.COMMAND, data)
                o1 = stdout.read().decode()
                o2 = stderr.read().decode()
                await websocket.send(json.dumps([o1, o2]))
        await websocket.close()
    except Exception as e:
        print(e)
        await websocket.close(reason=str(e))


async def main(): # 协程, 异步
    async with websockets.serve(handler, "0.0.0.0", 10800): # 监听，一个请求，一个Handler
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    asyncio.run(main()) # 大循环, 单线程
