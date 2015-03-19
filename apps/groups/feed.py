from feeds.helper import ModelFeed,Feeds
from groups.models import GroupActivity
from django.template.defaultfilters import urlize
from django.utils.html import escape

class GroupActivityFeed(ModelFeed):
  def content (self, instance, created):
    html = urlize(escape(instance.text).replace('\n','<br>'))
    tags = {
      'userwise':'true',
      'username':instance.group.user.username
    }
    return html, tags

  class Meta:
    model = GroupActivity
    app = 'groups'

Feeds.register(GroupActivityFeed)
