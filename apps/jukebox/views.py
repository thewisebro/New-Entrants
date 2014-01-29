"""
  Jukebox Views
"""

from core.views.generic import ListView,TemplateView,View,DetailView, RedirectView
from django.core import serializers
from django.http import HttpResponse
from django.core.urlresolvers import reverse
import simplejson
import json

from jukebox.models import *
from nucleus.models import User

from jukebox.serializers import *
from jukebox.permissions import *
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveAPIView
from rest_framework.response import Response
from itertools import chain

class IndexView(TemplateView):
  """
    For index page, i.e., starting page : For now -> Trending page
  """
  template_name='jukebox/base.html'
#url = 'search/'


class SearchView(ListView):
  """
    For three way search :  Song, Album, Artist
  """
  template_name='jukebox/search.html'
  model = Song
  def get_context_data(self,**kwargs):
    q = self.request.GET.get('q')                       # q -> Search String coming
    context = super(SearchView,self).get_context_data(**kwargs)
    songs1 = Song.objects.filter(song__istartswith=q)[:5]
    songs2 = Song.objects.filter(song__icontains=q).exclude(song__istartswith=q)[:5]
    songs = list(chain(songs1,songs2))
    songs = songs[:5]
    print songs
    artists1 = Artist.objects.filter(artist__istartswith=q)[:5]
    artists2 = Artist.objects.filter(artist__icontains=q).exclude(artist__istartswith=q)[:5]
    artists = list(chain(artists1,artists2))
    artists = artists[:5]
    albums1 = Album.objects.filter(album__istartswith=q)[:5]
    albums2 = Album.objects.filter(album__icontains=q).exclude(album__istartswith=q)[:5]
    albums = list(chain(albums1,albums2))
    albums = albums[:5]
    context.update({                                    # For multiple models and lists usage in ListView
        'songs' : songs,
        'albums' : albums,
        'artists' : artists,
    })
    return context


  """   songs = Song.objects.all()
  #songs_json = serializers.serialize("json", songs)
    songs_json = simplejson.dumps(songs)
    return HttpResponse(songs_json, mimetype="application/json")
  """



"""
Old Views: Without django rest framework

class TrendingView(ListView):
  ""
    For trending songs, i.e., count is maximum
  ""
  template_name = 'jukebox/trending.html'
  model = Song
  context_object_name = 'trending'
  def get_queryset(self):
    return Song.objects.order_by('-count')[:25]


class ArtistsView(ListView):
  ""
    To show a list of artists
  ""
  template_name = 'jukebox/artists.html'
  model = Artist
  context_object_name = 'artists'
  def get_queryset(self):
    return Artist.objects.all()


class AlbumsView(ListView):
  ""
    To show a list of albums
  ""
  template_name = 'jukebox/albums.html'
  model = Album
  context_object_name = 'albums'
  def get_queryset(self):
    return Album.objects.all()


class AlbumDescView(ListView):
  ""
    To show description of an Album, i.e., Artist, Songs, album_art
  ""
  template_name = 'jukebox/albumdesc.html'
  model = Album
  context_object_name = 'album'
  def get_queryset(self,**kwargs):
    if 'album' in self.kwargs:
      album_coming = self.kwargs['album']
      album = Album.objects.get(album = album_coming)
      return album


class ArtistDescView(ListView):
  ""
    To show description of an Artist, i.e., Albums, cover_pic
  ""
  template_name = 'jukebox/artistdesc.html'
  model = Artist
  context_object_name = 'artist'
  def get_queryset(self,**kwargs):
    if 'artist' in self.kwargs:
      artist_coming = self.kwargs['artist']
      artist = Artist.objects.get(artist = artist_coming)
      return artist
"""



"""
  Views for Playlists
"""

class PlaylistCreateView(RedirectView) :
  def get_redirect_url(self):
    user = self.request.user
    name = self.request.GET.get('name')                       # name -> name of Playlist Coming
    private = self.request.GET.get('private',False)                       # name -> name of Playlist Coming
    playlist = Playlist.objects.create(person=user, name=name, private=private)
    return reverse('playlist_all', kwargs={'user':user.username})
"""
class PlaylistAllView(ListView):
  template_name = 'jukebox/playlists.html'
  context_object_name = 'playlists'
  def get_queryset(self,**kwargs):
    if 'user' in self.kwargs:
      user_coming = self.kwargs['user']                      # user_coming --> user coming in url
      user_came = User.objects.get(username=user_coming)     # user_came = user object, user coming
      if self.request.user.is_active :
        user = self.request.user                             # user logged in
        if user.id == user_came.id :                         # If same user logged in... show all playlists
          playlists = Playlist.objects.filter(person=user.id)
        else :
          playlists = Playlist.objects.filter(person=user_came.id).exclude(private=True)  # If different user or no user logged in... show public playlists
      else :
        playlists = Playlist.objects.filter(person=user_came.id).exclude(private=True)
      return playlists
    else:
      pass


class PlaylistDescView(ListView):
  template_name = 'jukebox/playlistdesc.html'
  context_object_name = 'playlist'
  def get_queryset(self,**kwargs):
    if 'playlist' in self.kwargs:
      playlist_coming = self.kwargs['playlist']
      playlist = Playlist.objects.get(id = playlist_coming)
      return playlist

"""






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
    print self.request.user.username,self.request.POST.get('name','')
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











"""
  For Django-JSon Problem --> Not Resolved
"""
class JSONResponseMixin(object):
  def render_to_response(self, context):
    "Returns a JSON response containing 'context' as payload"
    return self.get_json_response(self.convert_context_to_json(context))

  def get_json_response(self, content, **httpresponse_kwargs):
    "Construct an `HttpResponse` object."
    return HttpResponse(content,
        content_type='application/json',
        **httpresponse_kwargs)

  def convert_context_to_json(self, context):
    "Convert the context dictionary into a JSON object"
# Note: This is *EXTREMELY* naive; in reality, you'll need
# to do much more complex handling to ensure that arbitrary
# objects -- such as Django model instances or querysets
# -- can be serialized as JSON.
    return json.dumps(context)


class ExampleView(JSONResponseMixin, View):
  def get(self, request, *args, **kwargs):
    #do some queries here to collect your data for the response
    json_response = "This ain't no country for old men"
    context = {'success':json_response}
    return self.render_to_response(context)
