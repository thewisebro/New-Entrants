from django.conf.urls import *

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('gate.views',
  (r'^gate/$', 'index'),
  (r'^gate_print_pdf/$','gate_print_pdf'),
  (r'^gate1/$', 'index1'),
)
