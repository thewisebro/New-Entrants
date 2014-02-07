from django.conf.urls import patterns, include, url

pagelet_patterns = patterns('nucleus.pagelets',
  url(r'^header/$', 'header', name='header'),
  url(r'^sidebar/$', 'sidebar', name='sidebar'),
)

urlpatterns = patterns('',
  url(r'^$', 'nucleus.views.index', name='notices_index'),
  url(r'^login', 'django.contrib.auth.views.login',
        {'template_name': 'nucleus/login.html'}, name='login'),
  url(r'^login_dialog/$', 'django.contrib.auth.views.login',
        {'template_name': 'nucleus/login_dialog.html'}, name='login_dialog'),
  url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page':'/'},
        name='logout'),
  url(r'^logout_ajax/$', 'nucleus.views.logout_ajax', name='logout_ajax'),
  url(r'^close_dialog/(?P<dialog_name>\w+)/$', 'nucleus.views.close_dialog',
        name='close_dialog'),
  url(r'', include(pagelet_patterns))
)
