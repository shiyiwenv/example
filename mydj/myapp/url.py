from django.conf.urls import url
from myapp import views

urlpatterns = [
    url(r"^index/", views.index, name='index')
]

