from django.conf.urls import patterns, url, include
from studentprofile import views

urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),
        url(r'^user/', include('oautherise.urls')),
        )