from django.conf.urls import url,patterns
from bunkometer.views import *
urlpatterns=patterns('',
    url('^$',bunkometer),
    url('^getsubjects/(?P<username>\d+)/$',getSubjects),
    url('^getbunks/(?P<username>\d+)/$',getBunks),
    url('^receive/(?P<username>\d+)/$',receive),
)
