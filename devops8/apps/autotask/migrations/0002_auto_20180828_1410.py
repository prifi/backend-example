# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-08-28 06:10
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('autotask', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='execresult',
            name='task',
        ),
        migrations.DeleteModel(
            name='ExecResult',
        ),
    ]