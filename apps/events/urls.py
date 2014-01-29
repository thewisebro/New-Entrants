from django.conf.urls import patterns, include, url
from api.filemanager import path_end

urlpatterns = patterns('events.views',
  (r'^add/$','add'),
  (r'^edit/(?P<event_id>\w+)/$','edit'),
  (r'^delete/$','delete'),
  (r'^get_calendars$','get_calendars'),
  (r'^fetch$','fetch'),
  (r'^get_events_dates$','get_events_dates'),
  (r'^browse/(?P<calendar_name>\w+)/'+path_end,'browse'),
)
