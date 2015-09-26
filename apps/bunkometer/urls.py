from django.conf.urls import url,patterns
from bunkometer.views import *
urlpatterns=patterns('',
    url('^$',bunkometer),
    url('^login/$',channeli_login),
    url('^checksession/$',check_session),
    url('^getsubjects/(?P<username>\d+)/$',getSubjects),
    url('^getbunks/(?P<username>\d+)/$',getBunks),
    url('^savetimetable/(?P<username>\d+)/$',saveTimeTable),
    url('^savebunks/(?P<username>\d+)/$',saveBunks),
    url('^gettimetable/(?P<username>\d+)/$',getTimeTable),
)
