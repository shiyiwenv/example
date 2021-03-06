# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-04-17 10:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0012_auto_20180411_1759'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='defaultBranch',
            field=models.CharField(blank=True, max_length=120, null=True, verbose_name='\u9ed8\u8ba4\u7248\u672c'),
        ),
        migrations.AlterField(
            model_name='project',
            name='gitVersion',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Git\u5206\u652f'),
        ),
        migrations.AlterField(
            model_name='project',
            name='postScriptPath',
            field=models.CharField(max_length=120, verbose_name='\u66f4\u65b0\u540e\u811a\u672c'),
        ),
        migrations.RemoveField(
            model_name='project',
            name='postServer',
        ),
        migrations.AddField(
            model_name='project',
            name='postServer',
            field=models.ManyToManyField(blank=True, null=True, related_name='postServer', to='myapp.Service'),
        ),
    ]
