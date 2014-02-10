from feeds.helper import ModelFeed
from django.template.loader import render_to_string
from events.models import Event

class EventFeed(ModelFeed):
  class Meta:
    model = Event
    app = 'events'

  def save(self, event, created):
    if not event.calendar.cal_type == 'PRI':
      return {
        'content': render_to_string('events/event_feed.html', {
            'event': event.serialize()
         }),
        'user': event.uploader if event.calendar.cal_type=='GRP' else None,
        'link': event.link
      }
    else:
      return None
