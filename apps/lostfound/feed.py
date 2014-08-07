from feeds.helper import ModelFeed,Feeds
from lostfound.models import LostItems, FoundItems 
from django.utils.html import escape

class LostFeed(ModelFeed):
  def content (self, instance, created):
    if not instance.status == 'Item found':
      html = instance.user.html_name() + ' lost ' + escape(instance.item_lost) + ' at ' + escape(instance.place) + '.'
      link = '/lostfound/view-item/lost/' + str(instance.pk)
      tags = {'link': link}
      return html, tags
    else:
      return None

  class Meta:
    model = LostItems
    app = 'lostfound'

class FoundFeed(ModelFeed):
  def content (self, instance, created):
    if not instance.status == 'Owner found':
      html = instance.user.html_name() + ' found ' + escape(instance.item_found) + ' at ' + escape(instance.place) + '.'
      link = '/lostfound/view-item/found/' + str(instance.pk)
      tags = {'link': link }
      return html, tags
    else:
      return None

  class Meta:
    model = FoundItems
    app = 'lostfound'

# Feeds.register(FoundFeed)
# Feeds.register(LostFeed)
