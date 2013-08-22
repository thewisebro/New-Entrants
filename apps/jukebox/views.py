"""
  Jukebox Views
"""

from core.views.generic import ListView,TemplateView,View,DetailView
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


class SearchView(ListView):
  template_name='jukebox/songlist.html'
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
