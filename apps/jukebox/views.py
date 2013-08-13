"""
  Jukebox Views
"""

from core.views.generic import ListView,TemplateView

from jukebox.models import Album,Artist,Song

class IndexView(TemplateView):
  template_name='jukebox/base.html'

class SearchView(ListView):
  template_name='jukebox/songlist.html'
  context_object_name = 'search_result'
  def get_queryset(self):
    return Song.objects.filter(song__istartswith='tt')[:5]
