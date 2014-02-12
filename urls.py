from django.conf.urls import patterns, include, url
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

actual_urlpatterns = patterns('',
  url(r'', include('nucleus.urls')),
  url(r'^feeds/', include('feeds.urls')),
  url(r'^events/', include('events.urls')),
  url(r'^lostfound/', include('lostfound.urls')),
  url(r'^crop_image/', include('crop_image.urls')),
  url(r'^admin/', include(admin.site.urls)),
  url(r'^jukebox/', include('jukebox.urls')),
  url(r'^helpcenter/', include('helpcenter.urls')),
  url(r'^taggit_autocomplete/', include('taggit_autocomplete.urls')),
  url(r'^media/(.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
  url(r'^songsmedia/(.*)$', 'django.views.static.serve', {'document_root': settings.JUKEBOX_MEDIA_ROOT}),
)

urlpatterns = patterns('',
  url(r'', include(actual_urlpatterns)),
  url(r'^u/(?P<account_username>\w+)/', include(actual_urlpatterns)),
)
