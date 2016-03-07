from feeds.helper import ModelFeed
from lostfound.models import LostItems, FoundItems
from django.template.loader import render_to_string

class LostFeed(ModelFeed):
  class Meta:
    model = LostItems
    app = 'lostfound'

  def save(self, instance, created):
    if not instance.status == 'Item found':
      instance.link = '/lostfound/view-item/lost/' + str(instance.pk)
      return {
        'content': render_to_string('lostfound/lost_feed.html',{
          'instance': instance,
        }),
        'user': instance.user,
        'link': instance.link,
      }
    else:
      return None

class FoundFeed(ModelFeed):
  class Meta:
    model = FoundItems
    app = 'lostfound'

  def save(self, instance, created):
    if not instance.status == 'Owner found':
      instance.link = '/lostfound/view-item/found/' + str(instance.pk)
      return {
        'content': render_to_string('lostfound/found_feed.html',{
          'instance': instance,
        }),
        'user': instance.user,
        'link': instance.link,
      }
    else:
      return None
