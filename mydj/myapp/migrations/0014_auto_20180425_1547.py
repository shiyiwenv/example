# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-04-25 07:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0013_auto_20180417_1818'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='postServer',
            field=models.ManyToManyField(blank=True, related_name='postServer', to='myapp.Service'),
        ),
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.CharField(default='0', max_length=120, null=True, verbose_name='Status'),
        ),
    ]
