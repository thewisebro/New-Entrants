from rest_framework import serializers
from notices.models import *

class NoticeListViewSerializer(serializers.ModelSerializer):
  class Meta:
    model = Notice
    fields = ('id', 'subject', 'uploader', 'datetime_modified')
    depth = 1

class GetNoticeSerializer(serializers.ModelSerializer):
  class Meta:
    model = Notice
    fields = ('id', 'reference', 'subject', 'uploader', 'content', 'datetime_modified')
    depth = 2
