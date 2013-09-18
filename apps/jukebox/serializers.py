from django.forms import widgets
from rest_framework import serializers
from jukebox.models import Song,Artist,Album


class SongSerializer(serializers.ModelSerializer):
  class Meta:
    model = Song
    fields = ('id', 'song', 'album', 'artists', 'count')
    depth = 1


class ArtistSerializer(serializers.ModelSerializer):
  class Meta:
    model = Artist
    fields = ('id', 'album_set', 'artist', 'cover_pic')
    depth = 1


class AlbumSerializer(serializers.ModelSerializer):
  class Meta:
    model = Album
    fields = ('id', 'song_set', 'album', 'artists', 'album_art')
    depth = 1
