from django.conf.urls import patterns, include, url

urlpatterns = patterns('games',
  (r'^$','views.index'),
  (r'^(?P<gamecode>\w+)/$','views.game'),
  (r'^(?P<gamecode>\w+)/authenticate/$','views.authenticate'),
  (r'^(?P<gamecode>\w+)/stop/$','views.stop'),
  (r'^(?P<gamecode>\w+)/highscores/$','views.highscores'),
  (r'^(?P<path>.*)$','views.index'),
)
