from django.conf.urls import patterns, url
from notices.views import *
urlpatterns = patterns('',
    url(r'^list_notices/(?P<page_no>\d+)/$', NoticeListView.as_view(), name='noticelist'),
    url(r'^upload/$', 'notices.views.upload', name='upload'), 
    url(r'^privelege/$', PrivelegeJsonView.as_view(), name = 'privelege'),
    url(r'^max_notices/$', Maxnumber.as_view(), name = 'max_number'),
    url(r'^get_notice/(?P<pk>\d+)/$', GetNotice.as_view(), name = 'getnotice')
)
