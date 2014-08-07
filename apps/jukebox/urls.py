from django.conf.urls import patterns, include, url
from django.conf.urls import *
from jukebox.views import *
import django

playlist_patterns = patterns('',

#    url(r'^create/', PlaylistCreateView.as_view(), name='create_playlist'),
#    url(r'^(?P<user>[\w\ ]+)/$', PlaylistAllView.as_view(), name='playlist_all'),
#    url(r'^(?P<user>[\w\ ]+)/(?P<playlist>[\w\ ]+)/$', PlaylistDescView.as_view(), name='playlist_desc'),


# Json starting
    url(r'^$', PlaylistAllJsonView.as_view(), name='playlist_all'),
    url(r'^(?P<pk>[0-9]+)/$', PlaylistDescView.as_view(), name='playlist_desc'),
)


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'channeli.views.home', name='home'),
    # url(r'^channeli/', include('channeli.foo.urls')),


    url(r'^$', IndexView.as_view(), name='index'),
#    url(r'^search/', SearchView.as_view(), name='search'),
#    url(r'^trending/$', TrendingView.as_view(), name='trending'),
#    url(r'^artists/$', ArtistsView.as_view(), name='artists'),
#    url(r'^albums/$', AlbumsView.as_view(), name='albums'),
#    url(r'^albums/(?P<album>[\w\ ]+)/$', AlbumDescView.as_view(), name='album_desc'),
#    url(r'^artists/(?P<artist>[\w\ ]+)/$', ArtistDescView.as_view(), name='artist_desc'),
#    url(r'^trending/play/$', PlayView.as_view(), name='count'),
    url(r'^login/$','jukebox.views.login' ),
    url(r'^logout/$','django.contrib.auth.views.logout' , {'next_page':'/jukebox/login'}),
    url(r'^playlists/', include(playlist_patterns)),

# Json Starting
    url(r'^trending/new/$', TemplateView.as_view(template_name='jukebox/trending_json.html')), # for practice
    url(r'^trending/$', TrendingJsonView.as_view()),
    url(r'^artists/$', ArtistsJsonView.as_view(), name='artists'),
    url(r'^albums/$', AlbumsJsonView.as_view(), name='albums'),
    url(r'^albums/(?P<id>[\d]+)/$', AlbumDescJsonView.as_view(), name='album_desc'),
    url(r'^artists/(?P<id>[\d]+)/$', ArtistDescJsonView.as_view(), name='artist_desc'),
    url(r'^play/$', PlayJsonView.as_view(), name='count'),
    url(r'^song/(?P<pk>[0-9]+)/$', GetSongView.as_view(), name='song_list'),
    url(r'^songs/$', SongsJsonView.as_view(), name='song_list'),
    url(r'^search/', SearchJsonView.as_view(), name='search'),
    url(r'^search_all/', SearchAllJsonView.as_view(), name='search_all'),
    url(r'^queue/', 'jukebox.views.getQueue', name='queue'),
    url(r'^playlists_add/$', AddToPlaylistView.as_view(), name='add_to_playlist'),
    url(r'^playlist_delete/$', DeletePlaylistView.as_view(), name='delete_playlist'),
    url(r'^playlist_rename/$', RenamePlaylistView.as_view(), name='rename_playlist'),
    url(r'^playlists_over/$', OverwritePlaylistView.as_view(), name='overwrite_playlist'),
    url(r'^playlist_delete_from/$', DeleteFromPlaylistView.as_view(), name='delete_from_playlist'),
    url(r'^playlist_change_index/$', ChangeIndexPlaylistView.as_view(), name='change_index_playlist'),
    url(r'^playlists_public/$', PublicPlaylistAllJsonView.as_view(), name='public_playlists'),
    url(r'^playlist_private_toggle/$', PublicPrivatePlaylistView.as_view(), name='public_private_playlist'),
)


