from django.conf.urls import patterns, include, url
from jukebox.views import *

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'channeli.views.home', name='home'),
    # url(r'^channeli/', include('channeli.foo.urls')),


    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^search/', SearchView.as_view(), name='search'),
    url(r'^trending/$', TrendingView.as_view(), name='trending'),
    url(r'^artists/$', ArtistsView.as_view(), name='artists'),
    url(r'^albums/$', AlbumsView.as_view(), name='albums'),
    url(r'^albums/(?P<album>[\w\ ]+)/$', AlbumDescView.as_view(), name='album_desc'),
    url(r'^artists/(?P<artist>[\w\ ]+)/$', ArtistDescView.as_view(), name='artist_desc'),
    url(r'^trending/play/$', PlayView.as_view(), name='count'),
)
