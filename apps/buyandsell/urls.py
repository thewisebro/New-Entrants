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
    url(r'^watch/(?P<mc>\w+)/?$', watch, name='watch main category'),
    url(r'^watch/(?P<mc>\w+)/(?P<c>\w+)/?$', watch, name='watch sub category'),
    url(r'^request_details/(?P<pk>\w+)/?$',requestdetails),
    url(r'^sell_details/(?P<pk>\w+)/?$',selldetails),
    url(r'^search/(?P<search_type>\w+)/?$',search),
    url(r'^see_all/(?P<search_type>\w+)/?$',seeall),
    url(r'^edit/(?P<form_type>\w+)/(?P<pk>\w+)/?$', edit,name='edit'),
    url(r'^trash/(?P<item_type>\w+)/(?P<pk>\w+)/?$', trash_item,name='trash'),
    url(r'^succ_trans/(?P<item_type>\w+)/(?P<pk>\w+)/?$', transaction,name='transaction'),
    url(r'^show_contact/(?P<response>\w+)/?$',show_contact,name='show_contact'),
    url(r'^manage/$', manage,name='manage_form'),
    url(r'^my-account/$', my_account),

 ) 
