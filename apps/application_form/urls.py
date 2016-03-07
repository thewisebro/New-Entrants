from django.conf.urls import *

urlpatterns = patterns ('application_form.views',
  (r'^$', 'app_form'),
  (r'^delete/$', 'delete_form'),
)


