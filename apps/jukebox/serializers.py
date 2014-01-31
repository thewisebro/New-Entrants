from HTMLParser import HTMLParser
from django.forms import widgets
from rest_framework import serializers
from jukebox.models import Song, Artist, Album, Playlist

class HyperlinkedFileField(serializers.FileField):
  def to_native(self, value):
    request = self.context.get('request', None)
    htm = HTMLParser()
    return htm.unescape(str(value.name))

class SongSerializer(serializers.ModelSerializer):
  file_name = HyperlinkedFileField(source='file_name')
  class Meta:
    model = Song
    fields = ('id', 'id_no', 'song', 'album', 'artists', 'count','file_name')
    depth = 1


class ArtistSerializer(serializers.ModelSerializer):
  class Meta:
    model = Artist
    fields = ('id', 'artist')
    depth = 1

class AlbumDescSerializer(serializers.ModelSerializer):
  class Meta:
    model = Album
    fields = ('id', 'song_set', 'album', 'artists', 'album_art')
    depth = 1

class ArtistDescSerializer(serializers.ModelSerializer):
  album_set = AlbumDescSerializer(many=True)
  class Meta:
    model = Artist
    fields = ('id', 'album_set', 'artist', 'cover_pic')
    depth = 1


class AlbumSerializer(serializers.ModelSerializer):
  class Meta:
    model = Album
    fields = ('id', 'album', 'artists')
    depth = 1


class PlaylistSerializer(serializers.ModelSerializer):
  person = serializers.Field(source='person.username')
  songs_list = serializers.SerializerMethodField('get_songs_list')
  class Meta:
    model = Playlist
    fields = ('id', 'songs', 'person', 'name', 'private','songs_list')
    depth = 2

  def get_songs_list(self, obj):
    if(obj==None):
      return []
    songs = obj.songs
    if(songs == ''):
      return []
    songs_id = songs.split('b')
    lsongs = Song.objects.in_bulk(songs_id)
    return lsongs


class PlayQueueSerializer(serializers.Serializer):
  songs = serializers.CharField()
  songs_list = serializers.SerializerMethodField('get_songs_list')
  def __init__(self,song_list, *args, **kwargs):
    self.songs = song_list
    super(PlayQueueSerializer,self).__init__(*args,**kwargs)
  class Meta:
    fields = ('songs_list')
    depth = 2

  def get_songs_list(self):
    if(songs == ''):
      return []
    songs_id = songs.split(',')
    lsongs = Song.objects.in_bulk(songs_id)
    return lsongs


