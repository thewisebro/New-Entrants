from django.conf.urls import patterns, url
from notices.views import *
urlpatterns = patterns('',
    url(r'^list_notices/(?P<llim>\d+)/(?P<hlim>\d+)/(?P<id>\d+)/$', NoticeListView.as_view(), name='noticelist'),
    url(r'^upload/$', 'notices.views.upload', name='upload'),
    url(r'^edit_notice/(?P<pk>\d+)/$', 'notices.views.edit', name = 'edit'),
    url(r'^delete_notice/(?P<pk>\d+)/$', 'notices.views.delete', name = 'delete'),
    url(r'^search/$', NoticeSearch.as_view() , name='search'),
    url(r'^read_star_notice/(?P<id1>\d+)/(?P<action>\w+)$', 'notices.views.read_star_notice' , name='read_star_action'),
    url(r'^mul_read_star_notice/(?P<action>\w+)/$', 'notices.views.mul_read_star_notice' , name='mul_read_star_action'),
    url(r'^max_notices/$',Maxnumber.as_view(), name='maxnumber'),
    url(r'^star_notice_list/$', Star_notice_list.as_view(), name='starred_list'),
    url(r'^read_notice_list/$', Read_notice_list.as_view(), name='read_list'),
    url(r'^show_uploads/$', Show_Uploads.as_view(), name='list_uploads'),
    url(r'^privelege/$', PrivelegeJsonView.as_view(), name = 'privelege'),
    url(r'^get_notice/(?P<pk>\d+)/$', GetNotice.as_view(), name = 'getnotice')
)
