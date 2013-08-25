"""
  Jukebox Views
"""

from core.views.generic import ListView,TemplateView,View,DetailView, RedirectView
from django.core import serializers
from django.http import HttpResponse
import simplejson
import json

from jukebox.models import Album,Artist,Song

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
    songs = Song.objects.filter(song__icontains=q)[:5]
    albums = Album.objects.filter(album__icontains=q)[:5]
    artists = Artist.objects.filter(artist__icontains=q)[:5]
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




class TrendingView(ListView):
  """
    For trending songs, i.e., count is maximum
  """
  template_name = 'jukebox/trending.html'
  model = Song
  context_object_name = 'trending'
  def get_queryset(self):
    return Song.objects.order_by('-count')[:25]


class ArtistsView(ListView):
  """
    To show a list of artists
  """
  template_name = 'jukebox/artists.html'
  model = Artist
  context_object_name = 'artists'
  def get_queryset(self):
    return Artist.objects.all()


class AlbumsView(ListView):
  """
    To show a list of albums
  """
  template_name = 'jukebox/albums.html'
  model = Album
  context_object_name = 'albums'
  def get_queryset(self):
    return Album.objects.all()


class AlbumDescView(ListView):
  """
    To show description of an Album, i.e., Artist, Songs, album_art
  """
  template_name = 'jukebox/albumdesc.html'
  model = Album
  context_object_name = 'album'
  def get_queryset(self,**kwargs):
    if 'album' in self.kwargs:
      album_coming = self.kwargs['album']
      album = Album.objects.get(album = album_coming)
      return album


class ArtistDescView(ListView):
  """
    To show description of an Artist, i.e., Albums, cover_pic
  """
  template_name = 'jukebox/artistdesc.html'
  model = Artist
  context_object_name = 'artist'
  def get_queryset(self,**kwargs):
    if 'artist' in self.kwargs:
      artist_coming = self.kwargs['artist']
      artist = Artist.objects.get(artist = artist_coming)
      return artist


class PlayView(View):
  """
    For Increasing the count
  """
  def get(self,request):
    song_id = self.request.GET['song_id']
    song = Song.objects.get(id=int(song_id))
    song.count += 1
    song.save()
    return HttpResponse('')








"""
  For Django-JSon Problem --> Not Resolved
"""
class JSONResponseMixin(object):  
  def render_to_response(self, context):  
    "Returns a JSON response containing 'context' as payload"  
    return self.get_json_response(self.convert_context_to_json(context))  

  def get_json_response(self, content, **httpresponse_kwargs):  
    "Construct an `HttpResponse` object."  
    return http.HttpResponse(content,  
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
