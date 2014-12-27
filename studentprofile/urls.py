from django.conf.urls import patterns, url, include
from studentprofile import views

urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),
        url(r'^user/', include('oautherise.urls')),
        url(r'^addlinks/', views.addlinks, name='addlinks'),
        url(r'^userprofile/(?P<userid>\w+)/$', views.userprofile, name='userprofile'),
        url(r'prof/(?P<userid>\w+)/$', views.userprofile, name='profile'),
        )