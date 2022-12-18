from django.db import models


class Cloud(models.Model):
    name = models.CharField("云厂商名称", max_length=50, help_text="云厂商名称")
    code = models.CharField("云厂商编号", max_length=50, help_text="云厂商编号")

    def __str__(self):
        return self.code


class Server(models.Model):
    cloud = models.ForeignKey(Cloud)
    instanceID = models.CharField("实例ID", max_length=50, db_index=True, help_text="实例ID")
    instanceType = models.CharField("实例类型", max_length=50, help_text="实例类型")
    cpu = models.CharField("CPU", max_length=50, db_index=True, help_text="实例CPU")
    memory = models.CharField("memory", max_length=50, help_text="实例内存")
    instanceName = models.CharField("实例名称", max_length=50, db_index=True, help_text="实例名称")
    createdTime = models.DateTimeField("创建时间", db_index=True, help_text="创建时间")
    expiredTime = models.DateTimeField("到期时间", db_index=True, help_text="到期时间")


class IP(models.Model):
    ip = models.GenericIPAddressField("IP", db_index=True, help_text="ip地址")
    inner = models.ForeignKey(Server, related_name="innerIP", null=True, help_text="内网IP")
    public = models.ForeignKey(Server, related_name="publicIP", null=True, help_text="外网IP")
