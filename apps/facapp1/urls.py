from django.conf.urls import patterns, url

from facapp import views

urlpatterns = patterns('',
  url(r'^$', views.home, name='home'),
  url(r'^fields/(?P<title>[\w\s]+)/$', views.sendFields, name='fields'),
  url(r'^createSection/', views.createSection, name='createSection'),
  url(r'^setPriority/', views.setPriority, name='setPriority'),
  )
