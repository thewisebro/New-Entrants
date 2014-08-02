from feeds.helper import ModelFeed,Feeds
from buysell.models import ItemsForSale, ItemsRequested 
from django.utils.html import escape

class ForSaleFeed(ModelFeed):
  def content (self, instance, created):
    html = instance.user.html_name() + " added " + escape(instance.item_name) + " for sale."
    if not 'images/buysell/default' in str(instance.item_image):
      html+="<br/><br/><img src='/media/"+str(instance.item_image)+"' />"
#      html+="<img src={{ MEDIA_URL }}{{ instance.item_image }}/>"
    link = '/buysell/buy_item_details/' + str(instance.pk)
    tags = {'link': link}
    return html, tags

  class Meta:
    model = ItemsForSale
    app = 'buysell'

class RequestedFeed(ModelFeed):
  def content (self, instance, created):
    html = instance.user.html_name() + " added a request for " + escape(instance.item_name) + "."
    link = '/buysell/requested_item_details/' + str(instance.pk)
    tags = {'link':link}
    return html, tags

  class Meta:
    model = ItemsRequested
    app = 'buysell'

Feeds.register(ForSaleFeed)
Feeds.register(RequestedFeed)
