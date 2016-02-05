from django.conf.urls import patterns, url
from new_entrants.views import *

urlpatterns = [
#    url(r'^seniors/$', seniors_list),
    url(r'^precheck/$', create_users),
    url(r'^blogs/$', blogs),
    url(r'^blogs/(?P<group_id>\w+)/$', blogs_group),
    url(r'blogs/(?P<group_id>\w+)/(?P<slug>[\w\-\(\)\&\:\,\?\!\.]+)/$', blogs_view),
    url(r'^connect/$', request_connect),
    url(r'^accept/$', accept_connect),
    url(r'^pending/$', pending_requests),
    url(r'^accepted/$',accepted),
    ]
