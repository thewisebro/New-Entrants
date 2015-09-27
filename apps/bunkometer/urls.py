from django.conf.urls import url,patterns
from bunkometer.views import *
urlpatterns=patterns('',
    url('^$',bunkometer),
    url('^login/$',channeli_login),
    url('^checksession/$',check_session),
    url('^getregisteredcourses/(?P<username>\d+)/$',getRegisteredCourses),
    url('^getcourses/(?P<username>\d+)/$', getCourses),
    url('^getbunks/(?P<username>\d+)/$',getBunks),
    url('^savetimetable/(?P<username>\d+)/$',saveTimeTable),
    url('^savebunks/(?P<username>\d+)/$',saveBunks),
    url('^savecourses/(?P<username>\d+)/$', saveCourses),
    url('^gettimetable/(?P<username>\d+)/$',getTimeTable),
)
