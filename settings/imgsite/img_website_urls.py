from django.conf.urls import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
  (r'', include('img_website.urls')),
  (r'^login/$', 'nucleus.views.login'),
  (r'^logout/$', 'nucleus.views.logout'),
  (r'^crop_image/', include('crop_image.urls')),
  (r'^redactor/', include('redactor.urls')),
)
