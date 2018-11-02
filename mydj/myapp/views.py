# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, HttpResponse
from django.contrib.auth import authenticate,login,logout
from myapp import models
from rest_framework_jwt.serializers import JSONWebTokenSerializer
from rest_framework_jwt.views import JSONWebTokenAPIView
from .renderers import APIRenderer
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.response import Response
from rest_framework import serializers
from myapp import serializers
from rest_framework import viewsets
from rest_framework.decorators import detail_route
# Create your views here.

def index(request):
    if  request.user.is_superuser:
        return render(request,'index.html')
    return render(request,'index1.html')
# def UserLogin(request):
#     if request.method == 'GET':
#         return render(request,'login.html')
#     else:
#         form = json.loads(request.body)
#         username = form['username']
#         password = form['password']
#         user = authenticate(username=username,password=password)
#         if user:
#             return JsonResponse({'code':'20000','message':u'登录成功'})
#         else:
#             return JsonResponse({'code':'30000','message':u'用户名或密码错误'})

def userlogout(request):
    logout(request)
    return HttpResponse('用户注销成功')

#用户登录验证api，DRF-jwt
class LoginTokenAPI(JSONWebTokenAPIView):
    serializer_class = JSONWebTokenSerializer


class hostAPI(viewsets.ModelViewSet):
    queryset = models.Service.objects.all()
    serializer_class = serializers.serviceSerializer

class ketAPI(viewsets.ModelViewSet):
    queryset = models.Key.objects.all()
    serializer_class = serializers.KeySerializer

    def perform_create(self, serializer):
        serializer.save(createUser=self.request.user)

    def perform_update(self, serializer):
        serializer.save(ChangeUser=self.request.user)

class projectAPI(viewsets.ModelViewSet):
    queryset = models.Project.objects.all()
    serializer_class = serializers.ProjectSerializer
    def dispatch(self, request, *args, **kwargs):
        # print (kwargs.get("pk"))
        return super(projectAPI, self).dispatch(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(createUser=self.request.user)

    def perform_update(self, serializer):
        serializer.save(changeUser=self.request.user)

    @detail_route(methods=['post'])
    def buildjob(self, request, pk=None):
        # print request, pk
        Preres= models.Project.objects.get(id=pk)
        print Preres.gitVersion
        models.oldTask.objects.create(
            projectid=Preres.id,
            name='',
            version=Preres.defaultBranch,
            git_version=Preres.gitVersion,
            email='',
            servers=Preres.postServer.all(),
            userid=Preres.createUser,
            repertory=Preres.gitVersion,
            before_secretkey='',
            before_server=Preres.preServer.ip,
            before_port=22022,
            before_user='build',
            before_script='/make.sh',
            before_config='',
            before_include='',
            channel_secretkey='',
            channel_server=Preres.middleServer.ip,
            channel_port=22022,
            channel_user='channel',
            after_secretkey='',
            after_user='',
            after_port=22022,
            after_script=Preres.postScriptPath,
            before_scriptbody=Preres.preScriptPath,
            target_path='' ,         #服务器目录
            push_path='/result',
            after_fileuser='',
            exclude=Preres.excludeList,
            full=Preres.sync,
            thread=Preres.threadNum,
            status=Preres.status,
            result='',
            full_result='',
            note='',
            createtime=Preres.createTime,
            modifytime=Preres.changeTime,
            created_at='0',
            updated_at='0'
        )
        return Response('success')

class TaskAPI(viewsets.ModelViewSet):
    queryset = models.Task.objects.all()
    serializer_class = serializers.TaskSerializer

    def perform_update(self, serializer):
        serializer.save(execUser=self.request.user)
class oldTaskAPI(viewsets.ModelViewSet):
    queryset = models.oldTask.objects.all()
    serializer_class = serializers.oldTaskSerializer

class StatusAPI(viewsets.ModelViewSet):
    queryset = models.Status.objects.all()
    serializer_class = serializers.StatusSerializer

class SysLogAPI(viewsets.ModelViewSet):
    queryset = models.SysLog.objects.all()
    serializer_class = serializers.SysLogSerializer

class ModuleAPI(viewsets.ModelViewSet):
    queryset = models.Module.objects.all()
    serializer_class = serializers.ModuleSerializer



@api_view(['GET'])
@renderer_classes((APIRenderer,))
def userinfo(request):
    return Response({
        'role': ['admin'] if request.user.is_superuser else ['user'],
        'token': ['admin'] if request.user.is_superuser else ['user'],
        'avatar': 'https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif',
        'name': request.user.last_name
    })

