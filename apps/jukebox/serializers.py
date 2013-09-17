from django.forms import widgets
from rest_framework import serializers
from jukebox.models import Song


class SongSerializer(serializers.ModelSerializer):
  class Meta:
    model = Song
    fields = ('id', 'song', 'album', 'artists', 'count')
    depth = 1
