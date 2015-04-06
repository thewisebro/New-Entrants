from feeds.helper import ModelFeed
from django.template.loader import render_to_string
from buysell.models import ItemsForSale, ItemsRequested

class ForSaleFeed(ModelFeed):
  class Meta:
    model = ItemsForSale
    app = 'buysell'

  def save(self, instance, created):
    instance.link = '/buysell/buy_item_details/' + str(instance.pk)
    return {
      'content': render_to_string('buysell/sale_feed.html', {
        'instance': instance,
      }),
      'user': instance.user,
      'link': instance.link,
    }

#html = instance.user.html_name() + " added " + escape(instance.item_name) + " for sale."
#if not 'images/buysell/default' in str(instance.item_image):
#html+="<br/><br/><img src='/media/"+str(instance.item_image)+"' />"
#      html+="<img src={{ MEDIA_URL }}{{ instance.item_image }}/>"
#link = '/buysell/buy_item_details/' + str(instance.pk)
#tags = {'link': link}
#return html, tags


class RequestedFeed(ModelFeed):
  class Meta:
    model = ItemsRequested
    app = 'buysell'

  def save(self, instance, created):
    instance.link = '/buysell/requested_item_details/' + str(instance.pk)
    return {
      'content': render_to_string('buysell/request_feed.html', {
        'instance': instance,
      }),
      'user': instance.user,
      'link': instance.link,
    }

#html = instance.user.html_name() + " added a request for " + escape(instance.item_name) + "."
#link = '/buysell/requested_item_details/' + str(instance.pk)
#tags = {'link':link}
#return html, tags
