from django.conf.urls import url,include
from django.contrib import admin
from myapp.views import LoginTokenAPI,hostAPI,ketAPI,projectAPI,TaskAPI,StatusAPI,SysLogAPI,ModuleAPI,userinfo,oldTaskAPI
from django.conf.urls import url, include
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets

# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'is_staff')

# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'hostApi',hostAPI)
router.register(r'keyApi',ketAPI)
router.register(r'ProApi',projectAPI)
router.register(r'TaskApi',TaskAPI)
router.register(r'oldtaskApi',oldTaskAPI)
router.register(r'StatusApi',StatusAPI)
router.register(r'SysLogApi',SysLogAPI)
router.register(r'ModuleApi',ModuleAPI)
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include(router.urls)),
    url(r'^api-token-auth/', LoginTokenAPI.as_view()),
    url(r'^api-auth/', include('rest_framework.urls')),
    url(r'^api/user/info', userinfo),
    url(r'^api/', include('myapp.url'))
]
