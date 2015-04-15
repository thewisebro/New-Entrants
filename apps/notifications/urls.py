from django.conf.urls import patterns, include, url

urlpatterns = patterns('notifications.views',
  (r'^fetch$', 'fetch'),
  (r'^mark_read$', 'mark_read'),
)
