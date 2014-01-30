"""
  Jukebox Views
"""
import json
from itertools import chain

from core.views.generic import ListView,TemplateView,View,DetailView, RedirectView
from django.core import serializers
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveAPIView
from rest_framework.response import Response

from nucleus.models import User
from jukebox.models import *
from jukebox.serializers import *
from jukebox.permissions import *

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
    obj.songs = ''
    obj.name = self.request.POST.get('name','')
    obj.private = True


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
    return Response(context)


