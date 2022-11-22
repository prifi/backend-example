# future

#### 介绍

权限管理系统，使用RBAC权限模型，实现菜单及页面标签元素的权限管控。

#### 软件架构

前端：Vue、Element
后端：Django
数据库：MySQL 5.7


#### 安装教程

后端：

```
1. 拉去代码
git clone https://gitee.com/yllan/future.git
cd future

2. 同步SQL文件到数据库中
common/db.sql

3. 同步数据 
python manage.py makemigrations
python manage.py migrate

4. 启动
python manage.py runserver
```

前端：

```
1. 拉取代码
git clone https://gitee.com/yllan/future-ui.git
cd future-ui

2. 安装依赖
npm install --registry=https://registry.npm.taobao.org
or
npm install -g cnpm --registry=https://registry.npm.taobao.org
cnpm install

3. 启动
npm run dev
```

默认配置：

```
1. 默认账号密码：lanyulei/lanyulei
   当然最好是自己创建用户：python manage.py createsuperuser

2. 账号配置为管理员，则拥有全部权限，不受角色权限限制。
```
