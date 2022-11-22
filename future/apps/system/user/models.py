#!/usr/bin/env python
# encoding: utf-8
# @author: lanyulei

from django.db import models
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser)


class UserInfoManager(BaseUserManager):
    def create_user(self, password=None, **kwargs):
        """
        Creates and saves a User with the given username, date of
        birth and password.
        """
        if not kwargs:
            raise ValueError('Users must have an username address')

        # 开始创建账号
        user = self.model(**kwargs)
        # 设置密码
        user.set_password(password)
        user.save(using=self._db)
        return user

    # 创建管理员
    def create_superuser(self, **kwargs):
        """
        Creates and saves a superuser with the given username, date of
        birth and password.
        """
        user = self.create_user(**kwargs)
        user.is_admin = True
        user.save(using=self._db)
        return user


# 在这里设置你需要的字段
class UserInfo(AbstractBaseUser):
    username = models.CharField(
        verbose_name='username',
        max_length=128,
        unique=True, )
    email = models.EmailField(
        verbose_name='email',
        max_length=255,
        null=True,
        blank=True,
        unique=True, )
    name = models.CharField(max_length=128, null=True, blank=True)
    is_active = models.BooleanField(verbose_name='是否可用', default=True)
    is_admin = models.BooleanField(verbose_name='是否管理员', default=False)
    create_date = models.DateTimeField(
        auto_now_add=True, blank=True, null=True)
    update_date = models.DateTimeField(blank=True, null=True, auto_now=True)
    objects = UserInfoManager()

    # 使用username作为必须的字段
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['name', 'email']

    def get_full_name(self):
        # The user is identified by their username address
        return self.username

    def get_short_name(self):
        # The user is identified by their username address
        return self.username

    def __unicode__(self):  # __unicode__ on Python 2
        return self.username

    def has_perm(self, perm, obj=None):
        """
        Return True if the user has the specified permission. Query all
        available auth backends, but return immediately if any backend returns
        True. Thus, a user who has permission from a single auth backend is
        assumed to have permission in general. If an object is provided, check
        permissions for that object.
        """
        # Active superusers have all permissions.
        if self.is_active and self.is_admin:
            return True

    def has_perms(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    class Meta:
        db_table = 'system_user'
