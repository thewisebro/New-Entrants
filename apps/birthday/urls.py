from django.conf.urls import patterns, include, url

urlpatterns = patterns('birthday.views',
  (r'^fetch$','fetch'),
  (r'^today$','today'),
  (r'^wish/(?P<username>\w+)/$','wish'),
  (r'^reply/(?P<message_id>\w+)/$', 'reply'),
)
