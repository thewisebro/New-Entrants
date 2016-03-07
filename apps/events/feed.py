from feeds.helper import ModelFeed
from django.template.loader import render_to_string
from django.contrib.auth.models import AnonymousUser
from events.models import Event
from events.views import event_dict

class EventFeed(ModelFeed):
  class Meta:
    model = Event
    app = 'events'

  def save(self, event, created):
    if event.calendar.cal_type == 'GRP':
      return {
        'content': render_to_string('events/event_feed.html', {
            'event': event_dict(event, AnonymousUser()),
            'uploader': event.uploader,
         }),
        'user': event.uploader,
        'link': event.link
      }
    else:
      return None
