from django.conf.urls.defaults import *

urlpatterns = patterns ('groups.views',
  (r'^$', 'index'),
  (r'^(?P<username>\w+)/$', 'group_details'),
  (r'^(?P<username>\w+)/admin_change/$', 'admin_change'),
  (r'^(?P<username>\w+)/edit/$', 'group_edit'),
  (r'^(?P<username>\w+)/members/$', 'group_members'),
  (r'^(?P<username>\w+)/events/$', 'group_events'),
  (r'^(?P<username>\w+)/activity/$', 'group_activity'),
  (r'^fetch_activities$','fetch_activities'),
  (r'^(?P<username>\w+)/add_member/$', 'member_add'),
  (r'^(?P<username>\w+)/add_multiple_member/$', 'member_add_multiple'),
  (r'^(?P<username>\w+)/delete_member/$', 'member_delete'),
  (r'^(?P<username>\w+)/add_post/$', 'post_add'),
  (r'^(?P<username>\w+)/delete_post/$', 'post_delete'),
  (r'^(?P<username>\w+)/change_post/$', 'post_change'),
  (r'^(?P<username>\w+)/subscriber/$', 'subscriber'),
  (r'^(?P<username>\w+)/activate/$', 'activate'),
) 
