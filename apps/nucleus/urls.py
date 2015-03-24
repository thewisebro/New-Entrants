from django.conf.urls import patterns, include, url

pagelet_patterns = patterns('nucleus.pagelets',
  url(r'^header_sidebar/$', 'header_sidebar', name='header_sidebar'),
)

urlpatterns = patterns('',
  url(r'^$', 'nucleus.views.index', name='index'),
  url(r'^login/$', 'django.contrib.auth.views.login',
        {'template_name': 'nucleus/login.html'}, name='login'),
  url(r'^login_dialog/$', 'django.contrib.auth.views.login',
        {'template_name': 'nucleus/login_dialog.html'}, name='login_dialog'),
  url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page':'/'},
        name='logout'),
  url(r'^logout_ajax/$', 'nucleus.views.logout_ajax', name='logout_ajax'),
  url(r'^close_dialog/(?P<dialog_name>\w+)/$', 'nucleus.views.close_dialog', name='close_dialog'),
  )

urlpatterns = patterns('nucleus.views',
  url(r'^$', 'index', name='index'),
  url(r'^login/$', 'login', name='login'),
  url(r'^login_dialog/$', 'login_dialog', name='login_dialog'),
  url(r'^logout/$', 'logout', name='logout'),
  url(r'^logout_ajax/$', 'logout_ajax', name='logout_ajax'),
  url(r'^close_dialog/(?P<dialog_name>\w+)/$', 'close_dialog', name='close_dialog'),
  url(r'^about/$', 'about', name='about'),
  url(r'^terms/$', 'terms', name='terms'),
  url(r'^hogwarts$', 'is_authenticate'),
  url(r'^get_links/$', 'get_links'),
  url(r'', include(pagelet_patterns))
)

urlpatterns += patterns('nucleus.media',
  (r'^photo/$','photo'),
  (r'^photo/(?P<username>\w+)/$','photo'),
)
