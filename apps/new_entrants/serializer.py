from rest_framework import serializers
from new_entrants.models import *
from django.conf import settings

class BlogSerializer(serializers.ModelSerializer):
  group_pic = serializers.SerializerMethodField('get_photo_link')
  name = serializers.SerializerMethodField('get_name')
  class Meta:
    model = Blog
    fields = ('title', 'description',  'content', 'date_published', 'name', 'group_pic')
    depth = 2

  def get_photo_link(slef, obj):
    link = ""
    if(settings.SITE!="INTRANET"):
      link = "http://people.iitr.ernet.in/photo/"
    else :
      link = "https://channeli.in/photo/"
    link += str(obj.user.username)
    return link

  def get_name(self, obj):
    return obj.name
