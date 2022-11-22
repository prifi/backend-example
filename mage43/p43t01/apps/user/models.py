from django.db import models

from django.contrib.auth.models import AbstractUser

# Create your models here.

# 扩展Django User模型
class UserProfile(AbstractUser):
    phone = models.CharField(max_length=32, verbose_name="电话号码", null=True, blank=True, help_text="电话号码")

    class Meta:
        db_table="auth_user"
        verbose_name = "用户详细信息"
        verbose_name_plural = verbose_name
