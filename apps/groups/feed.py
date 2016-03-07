from feeds.helper import ModelFeed
from groups.models import GroupActivity
from django.template.loader import render_to_string
from django.template.defaultfilters import urlize
from django.utils.html import escape

class GroupActivityFeed(ModelFeed):
  class Meta:
    model = GroupActivity
    app = 'groups'

  def save (self, instance, created):
    html = urlize(escape(instance.text)).replace('\n','<br>')
    return {
            'content':render_to_string('groups/groups_feed.html', {
                'instance':instance,
                'text':html
              }),
            'user':instance.group.user
    }
