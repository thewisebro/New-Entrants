from django.conf.urls import patterns, include, url
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

actual_urlpatterns = patterns('',
  url(r'', include('nucleus.urls')),
  url(r'^nucleus/', include('nucleus.urls')),
  url(r'^feeds/', include('feeds.urls')),
  url(r'^notifications/', include('notifications.urls')),
  url(r'^moderation/', include('moderation.urls')),
  url(r'^events/', include('events.urls')),
  url(r'^lostfound/', include('lostfound.urls')),
  url(r'^buysell/', include('buysell.urls')),
  url(r'^crop_image/', include('crop_image.urls')),
  url(r'^lectut_api/', include('lectut.urls')),
  url(r'^admin/', include(admin.site.urls)),
  url(r'^news/', include('news.urls')),
  url(r'^forum/', include('forum.urls')),
  url(r'^notices/', include('notices.urls')),
  url(r'^comments/', include('fluent_comments.urls')),
  url(r'^jukebox/', include('jukebox.urls')),
  url(r'^messmenu/', include('messmenu.urls')),
  url(r'^groups/', include('groups.urls')),
  url(r'^games/', include('games.urls')),
  url(r'^helpcenter/', include('helpcenter.urls')),
  url(r'^settings/', include('utilities.urls')),
  url(r'^birthday/', include('birthday.urls')),
  url(r'^placement/', include('placement.urls')),
  url(r'^internship/', include('internship.urls')),
  url(r'^softwares/', include('softwares.urls')),
  url(r'^taggit_autocomplete/', include('taggit_autocomplete.urls')),
  url(r'^media/(.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
  url(r'^peoplesearch/', include('peoplesearch.urls')),
  url(r'^newsmedia/(.*)$', 'django.views.static.serve', {'document_root': settings.NEWS_MEDIA_ROOT}),
  url(r'^songsmedia/(.*)$', 'django.views.static.serve', {'document_root': settings.JUKEBOX_MEDIA_ROOT}),
  url(r'^facapp/', include('facapp.urls')),
  url(r'^placement/', include('placement.urls')),
  url(r'^internship/', include('internship.urls')),
  url(r'^scholarships/', include('mcm.urls')),
  url(r'^songs/(.*)$', 'django.views.static.serve', {'document_root': settings.JUKEBOX_MEDIA_ROOT+'songs/'}),
  url(r'^genforms/', include('genforms.urls')),
  url(r'^gate/',include('gate.urls')),
)

urlpatterns = patterns('',
  url(r'', include(actual_urlpatterns)),
  url(r'^u/(?P<account_username>\w+)/', include(actual_urlpatterns)),
)

