from django.db import models

# Create your models here.

# ODM
from mongoengine import (
    Document, DynamicDocument,
    StringField, IntField, BooleanField, ListField,
    EmbeddedDocument, EmbeddedDocumentField
)

class CiTypeField(EmbeddedDocument):
    """嵌入文档 字段定义"""
    meta = {'collections': 'citypes', 'app_label': 'cmdb'}   # app_label 解决权限问题
    name = StringField(required=True, max_length=24)
    label = StringField(max_length=24)
    type = StringField(max_length=24)  # 自定义，可以是枚举
    required = BooleanField(default=False, required=True)

    def __str__(self):
        return "<CF {},{}>".format(self.name, self.type)


class CiType(Document):
    """类型定义"""
    meta = {
        'app_label': 'cmdb',
        'collection': 'citypes',
        'indexes': [
            'name',
            ('name', '-version')
        ],
        'ordering': ['-version']
    }
    name = StringField(required=True, unique_with='version', max_length=24)  # (name,version)联合唯一
    version = IntField(required=True, default=1)
    label = StringField()
    # flag = BooleanField(default=False)  # 表示该类型是否可以在下拉框中出现，被其他类型引用
    fields = ListField(EmbeddedDocumentField(CiTypeField))  # 子文档

    def __str__(self):
        return "<C {}:{}, {}>".format(self.name, self.version, self.fields)


# 1.空的model, 用于权限控制，生成基本权限 -- 迁移
# class Citype(models.Model):
#     # id
#     pass
#
# 2.自定义权限
# 手动在content_type及permissions中添加记录


class Ci(DynamicDocument):
    # 字段取决于CiType中某一类型在fields中定义的字段，几乎每种类型的字段都不一样
    meta = {'collection': 'cis'}
