# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    group = models.ForeignKey('Group')

    def __unicode__(self):
        return self.user.username

    class Meta:
        verbose_name = '用户表'
        verbose_name_plural = '用户表'


class Group(models.Model):
    name = models.CharField('组名', max_length=120)
    createTime = models.DateTimeField('创建时间', auto_now_add=True)
    changeTime = models.DateTimeField('修改时间', auto_now=True)
    project = models.ManyToManyField('Project')

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = '用户组'
        verbose_name_plural = '用户组'


class Project(models.Model):
    name = models.CharField('项目名', max_length=120)
    gitAddress = models.CharField('数据源', max_length=120)
    gitVersion = models.CharField('Git分支', max_length=50, null=True, blank=True)
    RocllgitVersion = models.CharField('回滚版本', max_length=50, null=True, blank=True)
    defaultBranch = models.CharField('默认版本', max_length=120, null=True, blank=True)
    middleServer = models.ForeignKey('Service', related_name='middleServer', null=True, blank=True)
    preServer = models.ForeignKey('Service', related_name='preServer', null=True, blank=True)
    postServer = models.ManyToManyField('Service', related_name='postServer', blank=True)
    preScriptPath = models.CharField('预处理脚本', max_length=120)
    pushMessage = models.CharField('推送通知', max_length=120,default='sa@sunteng.com')
    excludeList = models.TextField('排除列表')
    dstServerKey = models.ForeignKey('Key',null=True, blank=True)
    serverPort = models.IntegerField('服务器端口')
    postScriptPath = models.CharField('更新后脚本', max_length=120)
    threadNum = models.IntegerField('线程数', default=1)
    sync = models.BooleanField('完全同步', default=False)
    createTime = models.DateTimeField('创建时间', auto_now_add=True)
    createUser= models.ForeignKey(User, related_name='ProjectCreateUser')
    changeUser= models.ForeignKey(User, related_name='ProjectChangeUser', null=True, blank=True)
    changeTime = models.DateTimeField('修改时间', auto_now=True)
    isTemplate = models.BooleanField('是否为项目模板', default=False)
    backupPath = models.CharField('备份路径', max_length=120, null=True, blank=True)
    status = models.ForeignKey('Status',default='4')

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = '项目表'
        verbose_name = '项目表'


class Status(models.Model):
    name = models.CharField('状态名', max_length=20)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = '公共状态表'
        verbose_name = '公共状态表'


class Task(models.Model):
    log = models.TextField('任务执行日志')
    ip = models.ForeignKey('Service')
    percentage = models.IntegerField('进度条',default=0)
    execUser = models.ForeignKey(User)
    createTime = models.DateTimeField('创建时间', auto_now_add=True)
    project = models.ForeignKey('Project')

    def __unicode__(self):
        return '%s-%s' % (self.project.name, self.ip)

    class Meta:
        verbose_name_plural = '任务运行记录'
        verbose_name = '任务运行记录'

class oldTask(models.Model):
    projectid = models.IntegerField(null=True)
    name = models.CharField(max_length=128,null=True)
    version = models.CharField(max_length=128,null=True)
    gitversion = models.CharField(max_length=128,null=True)
    email = models.CharField(max_length=128,null=True)
    servers = models.TextField(null=True)
    userid = models.CharField(max_length=128,null=True)
    repertory = models.CharField(max_length=128,null=True)
    before_secretkey = models.TextField(null=True)
    before_server = models.CharField(max_length=128,null=True)
    before_port = models.IntegerField(null=True)
    before_user = models.CharField(max_length=128,null=True)
    before_script = models.CharField(max_length=128,null=True)
    before_config = models.TextField(null=True)
    before_include = models.TextField(null=True)
    channel_secretkey = models.TextField(null=True)
    channel_server = models.CharField(max_length=128,null=True)
    channel_port = models.IntegerField(null=True)
    channel_user =  models.CharField(max_length=128,null=True)
    after_secretkey =  models.TextField(null=True)
    after_user =  models.CharField(max_length=128,null=True)
    after_port = models.IntegerField(null=True)
    after_script =  models.CharField(max_length=128,null=True)
    before_scriptbody = models.TextField(null=True)
    target_path = models.CharField(max_length=128,null=True)
    push_path = models.CharField(max_length=128,null=True)
    after_fileuser = models.CharField(max_length=128,null=True)
    exclude = models.TextField(null=True)
    full = models.CharField(max_length=128,null=True)
    thread = models.IntegerField(null=True)
    status = models.IntegerField(null=True)
    result = models.TextField(null=True)
    full_result = models.TextField(null=True)
    note = models.TextField(null=True)
    created_at = models.CharField(max_length=128, null=True)
    updated_at = models.CharField(max_length=128, null=True)
    createtime = models.DateTimeField('创建时间', auto_now_add=True)
    modifytime = models.DateTimeField('写入时间', auto_now=True)

class SysLog(models.Model):
    log = models.TextField('系统日志信息')
    createTime = models.DateTimeField('创建时间', auto_now_add=True)
    changeTime = models.DateTimeField('写入时间', auto_now=True)

    def __unicode__(self):
        return self.createTime

    class Meta:
        verbose_name = '系统日志'
        verbose_name_plural = '系统日志'


class Service(models.Model):
    ip = models.GenericIPAddressField('主机ip')
    hostname = models.CharField('主机名', max_length=50)
    cpusum = models.IntegerField('cpu核心数',default=0)
    memory = models.CharField('内存大小',max_length=50)
    os_version = models.CharField('系统版本',max_length=50)
    postion = models.CharField('服务器位置',max_length=50)
    mode = models.CharField('服务器型号',max_length=50)
    ps = models.TextField('备注消息',max_length=1024)
    status = models.BooleanField('服务器状态',default=False)
    createTime = models.DateTimeField('创建时间', auto_now_add=True)
    changeTime = models.DateTimeField('修改时间', auto_now=True)

    def __unicode__(self):
        return '%s-%s' % (self.ip, self.hostname)

    class Meta:
        verbose_name = '主机管理'
        verbose_name_plural = '主机管理'


class Key(models.Model):
    name = models.CharField('名称', max_length=120)
    username = models.CharField('用户名', max_length=120)
    keyPath = models.CharField('私钥保存路径', max_length=120)
    password = models.CharField('私钥密码', max_length=120, null=True, blank=True)
    createUser = models.ForeignKey(User, related_name='KeyCreateUser')
    ChangeUser = models.ForeignKey(User, related_name='KeyChangeUser', null=True, blank=True)
    createTime = models.DateTimeField('创建时间', auto_now_add=True)
    changeTime = models.DateTimeField('修改时间', auto_now=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = '服务key'
        verbose_name_plural = '服务key'


class Module(models.Model):
    name = models.CharField('模块名称', max_length=120)
    project = models.ForeignKey('Project')
    createTime = models.DateTimeField('创建时间', auto_now_add=True)
    changeTime = models.DateTimeField('修改时间', auto_now=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = '模块名称'
        verbose_name_plural = '模块名称'
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles

LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted((item, item) for item in get_all_styles())


class Snippet(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    code = models.TextField()
    linenos = models.BooleanField(default=False)
    language = models.CharField(choices=LANGUAGE_CHOICES, default='python', max_length=100)
    style = models.CharField(choices=STYLE_CHOICES, default='friendly', max_length=100)

    class Meta:
        ordering = ('created',)