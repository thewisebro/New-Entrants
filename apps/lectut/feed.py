from feeds.helper import ModelFeed
from lectut.models import Post, Uploadedfile
from django.template.loader import render_to_string

class postFeed(ModelFeed):

  class Meta:
    model = Post
    app = 'lectut'

  def save(self, instance, created):
    instance.link = '/lectut/ajax/1/'
    return {
             'content': render_to_string('lectut/post_feed.html',{
             'instance': instance,
             }),
             'user': instance.upload_user,
             'link': instance.link,
           }
