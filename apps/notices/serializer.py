from rest_framework import serializers
from notices.models import *

class NoticeListViewSerializer(serializers.ModelSerializer):
  username = serializers.SerializerMethodField('get_username')
  category_name = serializers.SerializerMethodField('get_category')
  main_category = serializers.SerializerMethodField('get_main_category')
  class Meta:
    model = Notice
    fields = ('id', 'subject', 'uploader', 'datetime_modified', 'username', 'category_name', 'main_category')
    depth = 1

  def get_username(self, obj):
    return obj.uploader.user.username
  def get_category(self, obj):
    return obj.uploader.category.name
  def get_main_category(self, obj):
    return obj.uploader.category.main_category

class GetNoticeSerializer(serializers.ModelSerializer):
  username = serializers.SerializerMethodField('get_username')
  category = serializers.SerializerMethodField('get_category')
  class Meta:
    model = Notice
    fields = ('id', 'reference', 'subject', 'username', 'category' , 'content', 'datetime_modified')
    depth = 1

  def get_username(self, obj):
    return obj.uploader.user.username
  def get_category(self, obj):
    return obj.uploader.category.name
