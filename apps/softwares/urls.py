from django.conf.urls import *

urlpatterns = patterns('softwares.views',
    url(r'^$','index',name="download"),
    url(r'^browse/(?P<category>\w+)/$', 'browse', name='category'),
    url(r'^browse/(?P<category>\w+)/(?P<softwareid>\w+)/$', 'browse', name='browse'),
    url(r'^search/$', 'search', name='search'),
    url(r'^software_search/$', 'software_search'),
    url(r'^linux/$', 'index_linux'),
    url(r'^count/(?P<software_id>\w+)/$','download_count',name='download_count'),
    )
