from django.conf.urls import patterns, url

from facapp import views

urlpatterns = patterns('',
  url(r'^$', views.home, name='home'),

  )
