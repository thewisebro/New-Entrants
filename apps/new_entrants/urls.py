from django.conf.urls import patterns, url
from new_entrants.views import *

urlpatterns = patterns('',
    url(r'^$', index),  #true
    url(r'^userexists/$',userexists),  #true
    url(r'^register/$', register),  #true
    url(r'^userinfo/$', userinfo),  #true
    url(r'^blogs/$', blogs),  #true
    url(r'^blogs/(?P<group_id>\w+)/$', blogs_group),  #true
    url(r'blogs/(?P<group_id>\w+)/(?P<slug>[\w\-\(\)\&\:\,\?\!\.]+)/$', blogs_view),  #true
    url(r'^connect/$', request_connect),
    url(r'^accept/$', accept_connect),
    url(r'^pending/$', pending_requests),   #true
    url(r'^accepted/$', accepted),  #true
    )
