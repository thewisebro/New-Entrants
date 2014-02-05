from django.conf.urls import url, patterns
from lostfound.views import *

urlpatterns = patterns('',
    url(r'^$', index),
    url(r'^lost/$', lost),
    url(r'^found/$', found),
    url(r'^view-item/([^/]+)/([^/]+)/$', viewItem),
    url(r'^all/([^/]+)/$', allItems),
    url(r'^all/([^/]+)/([^/]+)/$', allItems),
    url(r'^account/$', account),
    url(r'^account/([^/]+)/$',account),
    url(r'^edit/([^/]+)/([^/]+)/$', edit),
    url(r'^delete/([^/]+)/([^/]+)/$', deleteEntry),
    url(r'^search/([^/]+)/([^/]+)/$', search),
    url(r'^status/([^/]+)/([^/]+)/$', status),
    url(r'^sendmail/([^/]+)/([^/]+)/$', sendmail),
    )
