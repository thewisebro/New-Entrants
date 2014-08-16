from django.conf.urls import patterns, include, url

pagelet_patterns = patterns('nucleus.pagelets',
  url(r'^header/$', 'header', name='header'),
  url(r'^sidebar/$', 'sidebar', name='sidebar'),
)

urlpatterns = patterns('nucleus.views',
  url(r'^$', 'index', name='index'),
  url(r'^login/$', 'login', name='login'),
  url(r'^login_dialog/$', 'login_dialog', name='login_dialog'),
  url(r'^logout/$', 'logout', name='logout'),
  url(r'^logout_ajax/$', 'logout_ajax', name='logout_ajax'),
  url(r'^close_dialog/(?P<dialog_name>\w+)/$', 'close_dialog',
        name='close_dialog'),
  url(r'^about/$', 'about', name='about'),
  url(r'^terms/$', 'terms', name='terms'),
  url(r'^hogwarts$', 'is_authenticate'),
  url(r'', include(pagelet_patterns))
)

urlpatterns += patterns('nucleus.media',
  (r'^photo/$','photo'),
  (r'^photo/(?P<username>\w+)/$','photo'),
)
