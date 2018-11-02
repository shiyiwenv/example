# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from models import *
# Register your models here.
admin.site.register([UserProfile,Group,Project,Status,Task,SysLog,Service,Key,Module])  #注册admin后台管理页面