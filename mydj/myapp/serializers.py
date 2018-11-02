from django.contrib.auth.models import User, Group
from rest_framework import serializers
from models import Snippet, LANGUAGE_CHOICES, STYLE_CHOICES
from myapp import models

class FormatTimeField(serializers.BaseSerializer):
   def to_representation(self, value):
       return value.strftime('%Y-%m-%d %H:%M %Z')
class StatusSerializer(serializers.ModelSerializer):
    name = serializers.CharField()

    class Meta:
        model = models.Status
        fields = '__all__'


class serviceSerializer(serializers.ModelSerializer):
    ip = serializers.IPAddressField()
    hostname = serializers.CharField()
    cpusum = serializers.IntegerField()
    memory = serializers.CharField()
    os_version = serializers.CharField()
    postion = serializers.CharField()
    mode = serializers.CharField()
    ps = serializers.CharField()
    status = serializers.BooleanField()
    class Meta:
        model = models.Service
        fields = '__all__'


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class KeySerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    username = serializers.CharField()
    keyPath = serializers.CharField()
    password = serializers.CharField()
    createTime = FormatTimeField(read_only=True)
    changeTime = FormatTimeField(read_only=True)
    ChangeUser = serializers.ReadOnlyField(required=False, source='ChangeUser.username',allow_null=True)
    createUser = serializers.ReadOnlyField(source='createUser.username', required=False, allow_null=True)

    # createUser = serializers.PrimaryKeyRelatedField(queryset=models.User.objects.all())

    class Meta:
        model = models.Key
        fields = '__all__'


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')


class ProjectSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    gitAddress = serializers.CharField()
    gitVersion = serializers.CharField()
    RocllgitVersion = serializers.CharField()
    defaultBranch = serializers.CharField()
    #dstServerKey = serializers.ReadOnlyField(source='dstServerKey.name', required=False, allow_null=True)
   # middleServer = serializers.ReadOnlyField(source='middleServer.ip', required=False, allow_null=True)
    #preServer = serializers.ReadOnlyField(source='preServer.ip', required=False, allow_null=True)
    #postServer = serializers.ReadOnlyField(source='postServer.ip', required=False,allow_null=True)
    preScriptPath = serializers.CharField()
    pushMessage = serializers.CharField()
    excludeList = serializers.CharField()
    serverPort = serializers.IntegerField()
    postScriptPath = serializers.CharField()
    threadNum = serializers.IntegerField()
    sync = serializers.BooleanField()
    isTemplate = serializers.BooleanField()
    backupPath = serializers.CharField()
    status = serializers.ReadOnlyField(source='status.name', allow_null=True)
    createTime = FormatTimeField(read_only=True)
    changeTime = FormatTimeField(read_only=True)
    changeUser = serializers.ReadOnlyField(required=False,
                                            source='changeUser.username', allow_null=True)
    createUser = serializers.ReadOnlyField(required=False,source='createUser.username', allow_null=True,read_only=True)


    class Meta:
        model = models.Project
        fields = '__all__'


class TaskSerializer(serializers.ModelSerializer):
    log = serializers.CharField()
    ip = serializers.ReadOnlyField(source='ip.ip', read_only=True)
    percentage = serializers.IntegerField()
    execUser = serializers.ReadOnlyField(source='execUser.username', read_only=True)
    project = serializers.ReadOnlyField(source='project.name', read_only=True)

    class Meta:
        model = models.Task
        fields = '__all__'
class oldTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.oldTask
        fields = '__all__'

class SysLogSerializer(serializers.ModelSerializer):
    log = serializers.CharField()

    class Meta:
        model = models.SysLog
        fields = '__all__'
class ModuleSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    project = serializers.ReadOnlyField(source='project.name', read_only=True)

    class Meta:
        model = models.Module
        fields = '__all__'

