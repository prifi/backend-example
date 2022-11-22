from django.db import models

# Create your models here.
from django.contrib.auth import get_user_model
UserProfile = get_user_model()

class Organization(models.Model):
    class Meta:
        db_table = 'js_org'
        verbose_name = '菜单表'
        verbose_name_plural = verbose_name

    name = models.CharField(max_length=48, verbose_name="菜单名称")
    parent = models.ForeignKey('self', on_delete=models.PROTECT, null=True, verbose_name="父ID") # 首级父节点为空
    is_delete = models.BooleanField(default=False) # 逻辑删除

    def __str__(self):
        return "<Org {},{}->{}>".format(self.pk, self.name, self.parent_id)


class Host(models.Model):
    class Meta:
        db_table = 'js_host'
        verbose_name = '主机表'
        verbose_name_plural = verbose_name

    org = models.ForeignKey(Organization, models.PROTECT, related_name='hosts')
    ip = models.GenericIPAddressField(blank=False, verbose_name="被管理主机IP")
    username = models.CharField(max_length=48, verbose_name="登录用户名")
    password = models.CharField(max_length=48, null=True, blank=True, verbose_name="登录密码")
    ssh_pkey_path = models.CharField(max_length=250, null=True, blank=True, verbose_name="私钥文件路径")
    is_delete = models.BooleanField(default=False)


class Track(models.Model):
    class Meta:
        db_table = 'js_tack'
        verbose_name = '审计表'
        verbose_name_plural = verbose_name

    class OPTYPES(models.IntegerChoices):
        LOGIN = (1, '登录')
        LOGOUT = (2, '登出')
        COMMAND = (3, '命令')

    user = models.ForeignKey(UserProfile, models.PROTECT, db_column='user_id')
    host = models.ForeignKey(Host, models.PROTECT, db_column='host_id')
    source_ip = models.GenericIPAddressField() # 支持IPv4, IPv6
    # op_type = models.IntegerField(choices=((1, '登录'), (2, '登出'), (3, '命令')))
    op_type = models.IntegerField(choices=OPTYPES.choices)
    op_date = models.DateTimeField(auto_now_add=True)
    command = models.CharField(max_length=255, null=True, blank=True, verbose_name="命令")
    op_state = models.BooleanField(verbose_name="执行结果状态")
