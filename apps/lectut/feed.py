from feeds.helper import ModelFeed
from lectut.models import Post, Uploadedfile
from django.template.loader import render_to_string

class postFeed(ModelFeed):

  class Meta:
    model = Post
    app = 'lectut'

  def save(self, instance, created):
    instance.link = '/lostfound/view-item/lost/' + str(instance.pk)
    return {
             'content': render_to_string('lostfound/lost_feed.html',{
             'instance': instance,
             }),
             'user': instance.user,
             'link': instance.link,
           }
