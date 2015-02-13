from django.conf.urls import url, patterns
from buyandsell.views import *

urlpatterns = patterns('',
    url(r'^buy()()/$', buy, name='none'),
    url(r'^buy/(?P<mc>\w+)/?$', buy, name='main category'),
    url(r'^buy/(?P<mc>\w+)/(?P<c>\w+)/?$', buy, name='sub category'),
    url(r'^viewrequests()()/$', viewrequests, name='none'),
    url(r'^viewrequests/(?P<mc>\w+)/?$', viewrequests, name='requests main category'),
    url(r'^viewrequests/(?P<mc>\w+)/(?P<c>\w+)/?$', viewrequests, name='requests sub category'),
    url(r'^sell/$', sell,name='sell form'),
    url(r'^requestitem/$', requestitem,name='request form'),
)
