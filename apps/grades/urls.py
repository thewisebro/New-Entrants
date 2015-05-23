from django.conf.urls.defaults import *

urlpatterns = patterns ('grades.views',
  (r'^$', 'index'),
  (r'^upload/$', 'upload'),
)
 
