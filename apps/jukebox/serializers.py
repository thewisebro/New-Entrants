from HTMLParser import HTMLParser
from django.forms import widgets
from rest_framework import serializers
from jukebox.models import *
#from jukebox.views import get_json_Queue

def get_json_Queue(song):
  htm = HTMLParser()
  return {
    'id':song.id,
    'album': song.album.album,
    'album_id':song.album.id,
    'album_art': song.album.album_art.name,
    'song':song.song,
    'file_name':htm.unescape(str( song.file_name.name)),
    'artist':song.artists.all()[0].artist,
    'artist_id':song.artists.all()[0].id,
  }

def get_json_album(album):
  return {
    'id':album.id,
    'album': album.album,
    'album_art': album.album_art.name,
    'artist':album.artists.all()[0].artist,
  }

def get_json_artist(artist):
  return {
    'id':artist.id,
    'artist':artist.artist,
    'cover_pic':artist.cover_pic.name,
  }

class HyperlinkedFileField(serializers.FileField):
  def to_native(self, value):
    request = self.context.get('request', None)
    htm = HTMLParser()
    return htm.unescape(str(value.name))

class AlbumArtSerializer(serializers.ModelSerializer):
  class Meta:
    model = Album
    fields = ('id', 'album', 'album_art')
    depth = 1


class ArtistSerializer(serializers.ModelSerializer):
  class Meta:
    model = Artist
    fields = ('id', 'artist')
    depth = 1

class SongSerializer(serializers.ModelSerializer):
  file_name = HyperlinkedFileField(source='file_name')
  album = AlbumArtSerializer()
  artists = ArtistSerializer(many=True)
  class Meta:
    model = Song
    fields = ('id', 'song', 'album', 'artists', 'file_name')
    depth = 1


class SongDescSerializer(serializers.ModelSerializer):
  file_name = HyperlinkedFileField(source='file_name')
  album = AlbumArtSerializer()
  artists = ArtistSerializer(many=True)
  class Meta:
    model = Song
    fields = ('id', 'id_no', 'song', 'album', 'artists', 'count','file_name')
    depth = 1


class ArtistSerializer(serializers.ModelSerializer):
  class Meta:
    model = Artist
    fields = ('id', 'artist')
    depth = 1

def get_songs_ser(x):
  try:
    return SongSerializer(x).data
  except:
    return None

class AlbumDescSerializer(serializers.ModelSerializer):
  song_set = serializers.SerializerMethodField('get_song_set')
  artists = ArtistSerializer(many=True)
  class Meta:
    model = Album
    fields = ('id', 'song_set', 'album', 'artists', 'album_art')
    depth = 2

  def get_song_set(self,obj):
    if(obj==None):
      return []
    songs = obj.song_set.all().order_by('id')
    songs = map(get_songs_ser, songs)
    return songs

class ArtistDescSerializer(serializers.ModelSerializer):
  album_set = AlbumDescSerializer(many=True)
  class Meta:
    model = Artist
    fields = ('id', 'album_set', 'artist', 'cover_pic')
    depth = 1


class AlbumSerializer(serializers.ModelSerializer):
  artists = ArtistSerializer(many=True)
  class Meta:
    model = Album
    fields = ('id', 'album', 'artists')
    depth = 1


class SearchArtistSerializer(serializers.ModelSerializer):
  artist_art = serializers.SerializerMethodField('get_artist_art')
  class Meta:
    model = Artist
    fields = ('id','artist','artist_art')

  def get_artist_art(self,obj):
    return obj.album_set.all()[0].album_art.name

class SearchAlbumSerializer(serializers.ModelSerializer):
  class Meta:
    model = Album
    fields = ('id', 'album', 'artists', 'album_art')
    depth = 1


class PlaylistSerializer(serializers.ModelSerializer):
  class Meta:
    model = Playlist
    fields = ('id', 'name')
    depth = 1

class PlaylistDescSerializer(serializers.ModelSerializer):
  person = serializers.Field(source='person.username')
  songs_list = serializers.SerializerMethodField('get_songs_list')
  owner = serializers.SerializerMethodField('get_owner')
  class Meta:
    model = Playlist
    fields = ('id', 'songs', 'name', 'songs_list', 'private', 'owner')
    depth = 2

  def get_songs_list(self, obj):
    if(obj==None):
      return []
    songs = obj.songs
    if(songs == ''):
      return []
    songs_id = songs.split('b')
    lsongs = Song.objects.in_bulk(songs_id)
    for key in lsongs.keys():
      lsongs[key]=SongSerializer(lsongs[key]).data

    return lsongs

  def get_owner(self, obj):
    request = self.context.get('request', None)
    if(request and request.user and request.user.username):                                           # if anonymous user user.username=''
      user = Jukebox_Person.objects.get_or_create(person=request.user)[0]                             # user logged in
      if user==obj.person:
        return True
      elif not obj.private:
        return obj.person.person.get_full_name()
    elif not obj.private:
      return obj.person.person.get_full_name()
    return False



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
    for key in lsongs.keys():
      lsongs[key]=SongSerializer(lsongs[key])
    return lsongs


