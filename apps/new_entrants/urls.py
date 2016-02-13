from django.conf.urls import patterns, url
from new_entrants.views import *

urlpatterns = patterns('',
#    url(r'^seniors/$', seniors_list)i,
    url(r'^register/$', register),
    url(r'^userinfo/$', userinfo),
    url(r'^blogs/$', blogs),  #true
    url(r'^blogs/(?P<group_id>\w+)/$', blogs_group),  #true
    url(r'blogs/(?P<group_id>\w+)/(?P<slug>[\w\-\(\)\&\:\,\?\!\.]+)/$', blogs_view),  #true
    url(r'^connect/$', request_connect),  #true
    url(r'^accept/$', accept_connect),  #true
    url(r'^pending/$', pending_requests),
    url(r'^accepted/$',accepted),  #truw
    )
