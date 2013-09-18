from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

actual_urlpatterns = patterns('',
  url(r'', include('nucleus.urls')),
  url(r'^admin/', include(admin.site.urls)),
)

urlpatterns = patterns('',
  url(r'', include(actual_urlpatterns)),
  url(r'^u/(?P<account_username>\w+)/', include(actual_urlpatterns)),
)
