"""
  Jukebox Views
"""
import json
from itertools import chain
from difflib import *
from HTMLParser import HTMLParser

from core.views.generic import ListView,TemplateView,View,DetailView, RedirectView
from django.core import serializers
from core.models import Q                                   # For complex lookups
from django.contrib.auth import authenticate
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


all_albums = open(JC.ALL_ALBUMS_JSON_FILE,'r+')
all_artists = open(JC.ALL_ARTISTS_JSON_FILE,'r+')
all_albums = json.loads(all_albums.readline())
all_artists = json.loads(all_artists.readline())

def dict_search(dictionary, search_field, search_str,limit=100):
  contains = []
  starts = []
  for key in dictionary.keys():
    if dictionary[key][search_field].lower().startswith(search_str):
      starts.append(dictionary[key])
    elif search_str in dictionary[key][search_field].lower():
      contains.append(dictionary[key])

    if len(starts) == limit:
      return starts
  return (starts + contains)[:limit]



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


def search_json(inp, dic):
  out = filter(lambda x: x.startswith(inp),dic.keys())
  if len(out)<5:
    out += filter(lambda x: (inp in x) and (not x.startswith(inp)),dic.keys())
  return out[:5]



def login(request):
  active = False
  if 'username' in request.POST and 'password' in request.POST:
    uid = request.POST['username']
    pwd = request.POST['password']
    if authenticate(username=uid, password=pwd):
      active = True
    else:
      active = False
  active = json.dumps({'active':active})
  return HttpResponse(active, mimetype='application/json')





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
  def get(self,request,*args, **kwargs):
    if 'id' in self.kwargs:
      album_coming = self.kwargs['id']
      album = all_albums[album_coming]
      return Response(album)
    """
  def get_queryset(self):
    if 'id' in self.kwargs:
      album_coming = self.kwargs['id']
      album = Album.objects.filter(id = album_coming)
      return album
    """


class ArtistDescJsonView(ListAPIView):
  """
    To show description of an Artist, i.e., Albums, cover_pic
  """
#serializer_class = ArtistDescSerializer
  def get(self,request,*args, **kwargs):
    if 'id' in self.kwargs:
      artist_coming = self.kwargs['id']
      artist = all_artists[artist_coming]
      return Response(artist)
  """def get_queryset(self):
    if 'id' in self.kwargs:
      artist_coming = self.kwargs['id']
      artist = Artist.objects.filter(id = artist_coming)
      return artist"""



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
    active = self.request.user.is_active
    if active :
      user = self.request.user                             # user logged in
      user = Jukebox_Person.objects.get_or_create(person=user)
      user = user[0]
      user.add_songs_listen(song)
    return Song.objects.filter(id=int(song_id))



class PlaylistAllJsonView(ListCreateAPIView):
  serializer_class = PlaylistSerializer
  permission_classes = (IsOwnerOrReadOnly,)
  def get(self,request):
    context = {}
    playlists = PlaylistSerializer(many=True)
    active = self.request.user.is_active
    if active :
      user = Jukebox_Person.objects.get_or_create(person=self.request.user)[0]                             # user logged in
      playlists = PlaylistSerializer(Playlist.objects.filter(person=user.id).order_by('-id'),many=True)
      context.update({                                    # For multiple models and lists usage in ListView
          'playlists' : playlists.data,
      })
    context.update({                                    # For multiple models and lists usage in ListView
        'active' : active,
    })
    return Response(context)


  def pre_save(self, obj):
    obj.person = Jukebox_Person.objects.get_or_create(person=self.request.user)[0]
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
      user = Jukebox_Person.objects.get_or_create(person=self.request.user)[0]                             # user logged in
      playlists = Playlist.objects.filter(person=user.id).filter(pk=playlist_id)
      if len(playlists) == 1 :
        playlist = playlists[0]
        if playlist.songs == '':
          playlist.songs = songs
        else:
          playlist.songs += 'b'+songs
        playlist.save()
    return Response('')



class OverwritePlaylistView(CreateAPIView):
  serializer_class = PlaylistSerializer
  permission_classes = (IsOwnerOrReadOnly,)
  def post(self,request):
    songs = self.request.POST.get('songs','')
    playlist_id = int(self.request.POST.get('id',''))
    active = self.request.user.is_active
    if active :
      user = Jukebox_Person.objects.get_or_create(person=self.request.user)[0]                             # user logged in
      playlists = Playlist.objects.filter(person=user.id).filter(pk=playlist_id)
      if len(playlists) == 1 :
        playlist = playlists[0]
        playlist.songs = songs
        playlist.save()
    return Response('')



class DeleteFromPlaylistView(CreateAPIView):
  serializer_class = PlaylistSerializer
  permission_classes = (IsOwnerOrReadOnly,)
  def post(self,request):
    index = int(self.request.POST.get('index',''))
    playlist_id = int(self.request.POST.get('id',''))
    active = self.request.user.is_active
    if active :
      user = Jukebox_Person.objects.get_or_create(person=self.request.user)[0]                             # user logged in
      playlists = Playlist.objects.filter(person=user.id).filter(pk=playlist_id)
      if len(playlists) == 1 :
        playlist = playlists[0]
        songs = playlist.songs.split('b')
        songs.pop(index)
        playlist.songs = 'b'.join(songs)
        playlist.save()
    return Response('')



class ChangeIndexPlaylistView(CreateAPIView):
  serializer_class = PlaylistSerializer
  permission_classes = (IsOwnerOrReadOnly,)
  def post(self,request):
    oindex = int(self.request.POST.get('oindex',''))
    nindex = int(self.request.POST.get('nindex',''))
    playlist_id = int(self.request.POST.get('id',''))
    active = self.request.user.is_active
    if active :
      user = Jukebox_Person.objects.get_or_create(person=self.request.user)[0]                             # user logged in
      playlists = Playlist.objects.filter(person=user.id).filter(pk=playlist_id)
      if len(playlists) == 1 :
        playlist = playlists[0]
        songs = playlist.songs.split('b')
        songs.insert(nindex,songs.pop(oindex))
        playlist.songs = 'b'.join(songs)
        playlist.save()
    return Response('')


class RenamePlaylistView(CreateAPIView):
  serializer_class = PlaylistSerializer
  permission_classes = (IsOwnerOrReadOnly,)
  def post(self,request):
    new_name = self.request.POST.get('name','')
    playlist_id = int(self.request.POST.get('id',''))
    active = self.request.user.is_active
    if active :
      user = Jukebox_Person.objects.get_or_create(person=self.request.user)[0]                             # user logged in
      playlists = Playlist.objects.filter(person=user.id).filter(pk=playlist_id)
      if len(playlists) == 1 :
        playlist = playlists[0]
        playlist.name = str(new_name)
        playlist.save()
    return Response('')

class DeletePlaylistView(CreateAPIView):
  serializer_class = PlaylistSerializer
  permission_classes = (IsOwnerOrReadOnly,)
  def post(self,request):
    playlist_id = int(self.request.POST.get('id',''))
    active = self.request.user.is_active
    if active :
      user = Jukebox_Person.objects.get_or_create(person=self.request.user)[0]                             # user logged in
      playlists = Playlist.objects.filter(person=user.id).filter(pk=playlist_id)
      if len(playlists) == 1 :
        playlist = playlists[0]
        playlist.delete()
    return Response('')


class PublicPrivatePlaylistView(CreateAPIView):
  serializer_class = PlaylistSerializer
  permission_classes = (IsOwnerOrReadOnly,)
  def get(self,request):
    playlist_id = int(self.request.POST.get('id',''))
    active = self.request.user.is_active
    if active :
      user = Jukebox_Person.objects.get_or_create(person=self.request.user)[0]                             # user logged in
      playlists = Playlist.objects.filter(person=user.id).filter(pk=playlist_id)
      if len(playlists) == 1 :
        playlist = playlists[0]
        playlist.private = not playlist.private
    return Response('')


class PublicPlaylistAllJsonView(ListAPIView):
  serializer_class = PlaylistSerializer
  def get_queryset(self):
    playlists = Playlist.objects.filter(private=False).order_by('-public_count')
    if self.request.user.is_active:
      user = Jukebox_Person.objects.get_or_create(person=self.request.user)[0]                             # user logged in
      playlists = playlists.exclude(person=user.id)
    return playlists



class PlaylistDescView(RetrieveAPIView):
#queryset = Playlist.objects.all()
  serializer_class = PlaylistDescSerializer
  def get_queryset(self):
    playlists = Playlist.objects.filter(private=False)
    active = self.request.user.is_active
    if active :
      user = Jukebox_Person.objects.get_or_create(person=self.request.user)[0]                             # user logged in
      playlists = Playlist.objects.filter(Q(person=user.id) | Q(private=False))
    return playlists



class GetSongView(RetrieveAPIView):
  queryset = Song.objects.all()
  serializer_class = SongSerializer


def map_queue(x):
  try:
    return int(x)
  except:
    pass
def getQueue(request):
  queue = request.GET['qu']
  queue = queue.split(',')
  queue = map(lambda x: map_queue(x), queue)
  lsongs = Song.objects.in_bulk(queue)
  for key in lsongs.keys():
    lsongs[key]=SongSerializer(lsongs[key]).data
  lsongs = json.dumps({'queue':lsongs})
  return HttpResponse(lsongs, mimetype='application/json')



class SearchJsonView(ListAPIView):
  """
    For three way search :  Song, Album, Artist
  """
  def get(self, request, format=None):
    context = {}
    q = self.request.GET.get('q').lower()                       # q -> Search String coming
    """context.update({                                    # For multiple models and lists usage in ListView
        'songs' : dict_search(songs,'song',q,5),
        'albums' : dict_search(albums,'album',q,5),
        'artists' : dict_search(artists,'artist',q,5),
    })"""
    songs1 = Song.objects.filter(song__istartswith=q)[:5]
    songs2 = Song.objects.filter(song__icontains=q).exclude(song__istartswith=q)[:5]
    songs = list(chain(songs1,songs2))
    songs = SongSerializer(songs[:5],many=True)
#print songs
    artists1 = Artist.objects.filter(artist__istartswith=q)[:5]
    artists2 = Artist.objects.filter(artist__icontains=q).exclude(artist__istartswith=q)[:5]
    artists = list(chain(artists1,artists2))
    artists = SearchArtistSerializer(artists[:5],many=True)
    albums1 = Album.objects.filter(album__istartswith=q)[:5]
    albums2 = Album.objects.filter(album__icontains=q).exclude(album__istartswith=q)[:5]
    albums = list(chain(albums1,albums2))
    albums = SearchAlbumSerializer(albums[:5],many=True)
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


class SearchAllJsonView(ListAPIView):
  """
    For three way search :  Song, Album, Artist
  """
  def get(self, request, format=None):
    context = {}
    q = self.request.GET.get('q').lower()                       # q -> Search String coming
    context.update({                                    # For multiple models and lists usage in ListView
        'songs' : dict_search(songs,'song',q),
    })
#song_keys = search_json(q.lower(),songs_search)
#print song_keys
    return Response(context)


