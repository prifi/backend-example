from django.db import models


# 模型分组
class ModelGroup(models.Model):
    name = models.CharField(verbose_name="名称", max_length=128)
    type = models.SmallIntegerField(verbose_name="类型")  # 1 模型分组，2 模型字段分组
    remarks = models.CharField(verbose_name="描述", max_length=1024)

    class Meta:
        db_table = "cmdb_model_group"


# 模型
class ModelInfo(models.Model):
    name = models.CharField(verbose_name="名称", max_length=128)
    icon = models.CharField(verbose_name="图标", max_length=45)
    tag = models.JSONField(verbose_name="标签")
    group = models.IntegerField(verbose_name="所属分组")

    class Meta:
        db_table = "cmdb_model"


# 字段
class Fields(models.Model):
    name = models.CharField(verbose_name="名称", max_length=128)
    type = models.CharField(verbose_name="类型", max_length=128)  # 例如：string 字符串，int 整数...
    is_unique = models.BooleanField(verbose_name="是否唯一", default=False)
    required = models.BooleanField(verbose_name="是否必填", default=False)
    prompt = models.CharField(verbose_name="用户提示", max_length=256)
    group = models.IntegerField(verbose_name="分组")
    model = models.IntegerField(verbose_name="模型")
    is_list = models.BooleanField(verbose_name="是否列表展示", default=True)
    sort = models.SmallIntegerField(verbose_name="顺序")
    default = models.CharField(verbose_name="默认值", max_length=256)
    configuration = models.JSONField(verbose_name="字段不同类型的配置数据")  # 例如数字的最大，最小，步长，单位等数据

    class Meta:
        db_table = "cmdb_model_fields"


# 资源分组
class Resource(models.Model):
    model = models.CharField(verbose_name="模型", max_length=128)
    data = models.JSONField(verbose_name="模型")

    class Meta:
        db_table = "cmdb_resource"


# 资源关联
class ResourceRelated(models.Model):
    source = models.IntegerField(verbose_name="源数据ID")
    target = models.IntegerField(verbose_name="源数据ID")

    class Meta:
        db_table = "cmdb_resource_related"


# 云账号管理
class CloudAccount(models.Model):
    name = models.CharField(verbose_name="名称", max_length=128)
    type = models.CharField(verbose_name="类型", max_length=128)  # 阿里云、百度云、腾讯云等等
    status = models.BooleanField(verbose_name="状态", default=True)
    secret = models.CharField(verbose_name="accessSecret", max_length=128)
    key = models.CharField(verbose_name="accessKeyID", max_length=128)
    remarks = models.CharField(verbose_name="备注", max_length=1024)

    class Meta:
        db_table = "cmdb_cloud_account"


# 云资源同步
class CloudDiscovery(models.Model):
    name = models.CharField(verbose_name="名称", max_length=128)
    model = models.IntegerField(verbose_name="绑定模型")
    could_account = models.IntegerField(verbose_name="云账号")
    region = models.JSONField(verbose_name="区域")
    status = models.BooleanField(verbose_name="状态")
    last_sync_status = models.BooleanField(verbose_name="最近同步状态")
    last_sync_time = models.DateTimeField(verbose_name="最近同步时间")
    remarks = models.CharField(verbose_name="备注", max_length=1024)

    class Meta:
        db_table = "cmdb_cloud_discovery"
