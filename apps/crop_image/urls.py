from django.conf.urls import patterns, include, url

urlpatterns = patterns('crop_image',
  url(r'^upload_image/(?P<unique_name>\w+)/(?P<pk>\w+)/$', 'views.upload_image', name='upload_image'),
)

