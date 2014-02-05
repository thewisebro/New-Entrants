"""
  Jukebox Views
"""
import json
from itertools import chain
from difflib import *

from core.views.generic import ListView,TemplateView,View,DetailView, RedirectView
from django.core import serializers
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveAPIView, CreateAPIView
from rest_framework.response import Response

from nucleus.models import User
from jukebox.models import *
from jukebox.serializers import *
from jukebox.permissions import *
from jukebox import constants as JC

songs = open(JC.SONGS_JSON_FILE,'r+')
albums = open(JC.ALBUMS_JSON_FILE,'r+')
artists = open(JC.ARTISTS_JSON_FILE,'r+')

songs = songs.readline()
albums = albums.readline()
artists = artists.readline()

songs = json.loads(songs)
albums = json.loads(albums)
artists = json.loads(artists)

songs_search = {}
for key in songs.keys():
  songs_search[songs[key]['song'].lower()]=key


albums_search = {}
for key in albums.keys():
  albums_search[albums[key]['album'].lower()]=key

artists_search = {}
for key in artists.keys():
  artists_search[artists[key]['artist'].lower()]=key


def search_json(inp, dic):
  out = filter(lambda x: x.startswith(inp),dic.keys())
  if len(out)<5:
    out += filter(lambda x: (inp in x) and (not x.startswith(inp)),dic.keys())
  return out[:5]

class IndexView(TemplateView):
  """
    For index page, i.e., starting page : For now -> Trending page
  """
  template_name='jukebox/base.html'
#url = 'search/'


"""
  For JSON Response
"""
class TrendingJsonView(ListAPIView):
  queryset = Song.objects.order_by('-count')[:50]
  serializer_class = SongSerializer


class ArtistsJsonView(ListAPIView):
  """
    To show a list of artists
  """
  queryset = Artist.objects.order_by('artist')
  serializer_class = ArtistSerializer


class AlbumsJsonView(ListAPIView):
  """
    To show a list of albums
  """
  queryset = Album.objects.order_by('album')
  serializer_class = AlbumSerializer


class SongsJsonView(ListAPIView):
  """
    To show a list of artists
  """
  queryset = Song.objects.all()
  serializer_class = SongSerializer


class AlbumDescJsonView(ListAPIView):
  """
    To show description of an Album, i.e., Artist, Songs, album_art
  """
  serializer_class = AlbumDescSerializer
  def get_queryset(self):
    if 'id' in self.kwargs:
      album_coming = self.kwargs['id']
      album = Album.objects.filter(id = album_coming)
      return album


class ArtistDescJsonView(ListAPIView):
  """
    To show description of an Artist, i.e., Albums, cover_pic
  """
  serializer_class = ArtistDescSerializer
  def get_queryset(self):
    if 'id' in self.kwargs:
      artist_coming = self.kwargs['id']
      artist = Artist.objects.filter(id = artist_coming)
      return artist



class PlayJsonView(ListAPIView):
  """
    For Increasing the count
  """
  serializer_class = SongSerializer
  def get_queryset(self):
    song_id = self.request.GET['song_id']
    song = Song.objects.get(id=int(song_id))
    song.count += 1
    song.save()
    return Song.objects.filter(id=int(song_id))



class PlaylistAllJsonView(ListCreateAPIView):
  serializer_class = PlaylistSerializer
  permission_classes = (IsOwnerOrReadOnly,)
  def get(self,request):
    context = {}
    playlists = PlaylistSerializer(many=True)
    active = self.request.user.is_active
    if active :
      user = self.request.user                             # user logged in
      playlists = PlaylistSerializer(Playlist.objects.filter(person=user.id).order_by('-id'),many=True)
      context.update({                                    # For multiple models and lists usage in ListView
          'playlists' : playlists.data,
      })
    context.update({                                    # For multiple models and lists usage in ListView
        'active' : active,
    })
    return Response(context)


  def pre_save(self, obj):
    obj.person = self.request.user
    obj.songs = self.request.POST.get('songs','')
    obj.name = self.request.POST.get('name','')
    obj.private = True


class AddToPlaylistView(CreateAPIView):
  serializer_class = PlaylistSerializer
  permission_classes = (IsOwnerOrReadOnly,)
  def post(self,request):
    songs = self.request.POST.get('songs','')
    playlist_id = int(self.request.POST.get('id',''))
    active = self.request.user.is_active
    if active :
      user = self.request.user                             # user logged in
      playlists = Playlist.objects.filter(person=user.id).filter(pk=playlist_id)
      if len(playlists) == 1 :
        playlist = playlists[0]
        playlist.songs += 'b'+songs
        playlist.save()
    return Response('')



class PlaylistDescView(RetrieveAPIView):
#queryset = Playlist.objects.all()
  serializer_class = PlaylistSerializer
  def get_queryset(self):
    active = self.request.user.is_active
    if active :
      user = self.request.user                             # user logged in
      playlists = Playlist.objects.filter(person=user.id)
      return playlists

class GetSongView(RetrieveAPIView):
  queryset = Song.objects.all()
  serializer_class = SongSerializer

def get_json_Queue(song):
  return {
    'id':song.id,
    'album': song.album.album,
    'album_art': song.album.album_art.name,
    'song':song.song,
    'artist':song.artists.all()[0].artist,
  }

def getQueue(request):
  queue = request.GET['qu']
  queue = queue.split(',')
  queue = map(lambda x: int(x), queue)
  lsongs = Song.objects.in_bulk(queue)
  for key in lsongs.keys():
    lsongs[key]=get_json_Queue(lsongs[key])
  lsongs = json.dumps({'queue':lsongs})
  return HttpResponse(lsongs, mimetype='application/json')



class SearchJsonView(ListAPIView):
  """
    For three way search :  Song, Album, Artist
  """
  def get(self, request, format=None):
    context = {}
    q = self.request.GET.get('q')                       # q -> Search String coming
    songs1 = Song.objects.filter(song__istartswith=q)[:5]
    songs2 = Song.objects.filter(song__icontains=q).exclude(song__istartswith=q)[:5]
    songs = list(chain(songs1,songs2))
    songs = SongSerializer(songs[:5],many=True)
#print songs
    artists1 = Artist.objects.filter(artist__istartswith=q)[:5]
    artists2 = Artist.objects.filter(artist__icontains=q).exclude(artist__istartswith=q)[:5]
    artists = list(chain(artists1,artists2))
    artists = ArtistSerializer(artists[:5],many=True)
    albums1 = Album.objects.filter(album__istartswith=q)[:5]
    albums2 = Album.objects.filter(album__icontains=q).exclude(album__istartswith=q)[:5]
    albums = list(chain(albums1,albums2))
    albums = AlbumSerializer(albums[:5],many=True)
# songs = SongSerializer(Song.objects.filter(song__icontains=q)[:5],many=True)
#albums = AlbumSerializer(Album.objects.filter(album__icontains=q)[:5],many=True)
#artists = ArtistSerializer(Artist.objects.filter(artist__icontains=q)[:5], many=True)
    context.update({                                    # For multiple models and lists usage in ListView
        'songs' : songs.data,
        'albums' : albums.data,
        'artists' : artists.data,
    })
#song_keys = search_json(q.lower(),songs_search)
#print song_keys
    return Response(context)


