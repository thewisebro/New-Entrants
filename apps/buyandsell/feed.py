from feeds.helper import ModelFeed
from django.template.loader import render_to_string
from buyandsell.models import SaleItems, RequestedItems

class saleFeed(ModelFeed):
  class Meta:
    model = SaleItems
    app = 'buyandsell'

  def save(self, instance, created):
    instance.link = '/buyandsell/sell_details/' + str(instance.pk)
    return {
      'content': render_to_string('buyandsell/sale_feed.html', {
        'instance': instance,
      }),
      'user': instance.user,
      'link': instance.link,
    }


class requestFeed(ModelFeed):
  class Meta:
    model = RequestedItems
    app = 'buyandsell'

  def save(self, instance, created):
    instance.link = '/buyandsell/request_details/' + str(instance.pk)
    return {
      'content': render_to_string('buyandsell/request_feed.html', {
        'instance': instance,
      }),
      'user': instance.user,
      'link': instance.link,
    }

