from django.conf.urls import *

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('gate.views',
  (r'^gate/$', 'index'),
)
