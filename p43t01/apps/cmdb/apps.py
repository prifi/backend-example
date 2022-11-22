from django.apps import AppConfig
from django.conf import settings
from mongoengine import connect, connection


class CmdbConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.cmdb'
    flag = False  # 标志位，判断仅加载一次

    def ready(self):
        print('~~CMDB项目启动时加载，建立MonogDB连接~~')
        if not self.flag:
            connect(**settings.MONGODB_DATABASES)
            self.flag = True
        # MongoDB数据库连接全局配置
        print('-'*50)
        print(connection._connections)
        print(connection._connection_settings)
        print('-' * 50)
