from feeds.helper import ModelFeed
from lectut.models import Post, Uploadedfile
from django.template.loader import render_to_string

class postFeed(ModelFeed):

  class Meta:
    model = Post
    app = 'lectut'

  def save(self, instance, created):
    instance.link = '/lectut/#/course/'+str(instance.batch.id)+'/feeds/'+str(instance.id)+'/'
    Files = Uploadedfile.file_objects.filter(post = instance).all()
    file_details = []
    for someFile in Files:
      link = '/lectut/#/course/'+str(instance.batch.id)+'/files/'+str(someFile.id)+'/'
      data = {'file_name':str(someFile.upload_file).split['/'][2] , 'file_link':link}
      file_details.append(data)
    instance.count = len(Files)
    return {
             'content': render_to_string('lectut/post_feed.html',{
             'instance': instance,
             }),
             'user': instance.upload_user,
             'link': instance.link,
             'count':instance.count,
             'files':file_details
           }
