from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
  url(r'^$', 'nucleus.views.index', name='index'),
  url(r'^login/$', 'django.contrib.auth.views.login',
    {'template_name': 'nucleus/login.html'}, name='login'),
  url(r'^logout/$', 'django.contrib.auth.views.logout_then_login', name='logout'),
)
