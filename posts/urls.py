from django.conf.urls import url
from . import views

app_name = 'posts'

urlpatterns = [
    url(r'^create/', views.create, name='create'),
    url(r'^(?P<pk>[0-9]+)/detail', views.detail, name='detail'),
    url(r'^userposts/', views.userposts, name='userposts'),
    url(r'^delete/(?P<id>\d+)/$', views.delete),
]
