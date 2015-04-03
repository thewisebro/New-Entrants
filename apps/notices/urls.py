from django.conf.urls import patterns, url
from notices.views import *
from filemanager import path_end
from django.contrib.auth.decorators import login_required

urlpatterns = patterns('',
    url(r'^upload/$', 'notices.views.upload', name='upload'),
    url(r'^edit_notice/(?P<pk>\d+)/$', 'notices.views.edit', name = 'edit'),
    url(r'^delete_notice/(?P<pk>\d+)/$', 'notices.views.delete', name = 'delete'),
    url(r'^search/(?P<mode>\w+)/(?P<mc>\w+)/(?P<subc>[\w\ ]+)/$', NoticeSearch.as_view() , name='search'),
    url(r'^read_star_notice/(?P<id1>\d+)/(?P<action>\w+)$', 'notices.views.read_star_notice' , name='read_star_action'),
    url(r'^mul_read_star_notice/(?P<action>\w+)/$', 'notices.views.mul_read_star_notice' , name='mul_read_star_action'),
    url(r'^max_notices/$' ,Maxnumber.as_view(), name='maxnumber'),
    url(r'^star_notice_list/$', login_required(Show_Starred.as_view()), name='starred_list'),
    url(r'^read_notice_list/$', login_required(Read_notice_list.as_view()), name='read_list'),
    url(r'^show_uploads/$', Show_Uploads.as_view(), name='list_uploads'),
    url(r'^privelege/$', PrivelegeJsonView.as_view(), name = 'privelege'),
    url(r'^get_constants/$', GetConstants.as_view(), name = 'privelege'),
    url(r'^get_notice/(?P<pk>\d+)/$', GetNotice.as_view(), name = 'getnotice'),
    url(r'^temp_max_notices/(?P<mode>\w+)/(?P<mc>\w+)/(?P<subc>[\w\ ]+)/$', TempMaxNotice.as_view(), name = 'getnotice'),
    url(r'^content_first_time_notices1/(?P<nid>\w+)/$', ContentFirstTimeBringNotices1.as_view(), name = 'getnotice'),
    url(r'^content_first_time_notices2/$', ContentFirstTimeBringNotices2.as_view(), name = 'getnotice'),
    url(r'^list_notices/(?P<mode>\w+)/(?P<mc>\w+)/(?P<subc>[\w\ ]+)/(?P<llim>\d+)/(?P<hlim>\d+)/(?P<id>\d+)/$', NoticeListView.as_view(), name='noticelist'),
    url(r'^browse/(?P<category_name>\w+)/$'+path_end,'notices.views.browse'),
)
