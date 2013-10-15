from django.forms import widgets
from rest_framework import serializers
from jukebox.models import Song,Artist,Album, Playlist




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




