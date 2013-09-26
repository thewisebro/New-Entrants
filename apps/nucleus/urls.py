from django.conf.urls import patterns, include, url

pagelet_patterns = patterns('',
  url(r'^header/$', 'nucleus.pagelets.header', name='header')
)

urlpatterns = patterns('',
  url(r'^$', 'nucleus.views.index', name='index'),
  url(r'^login/$', 'django.contrib.auth.views.login',
        {'template_name': 'nucleus/login.html'}, name='login'),
  url(r'^login_dialog/$', 'django.contrib.auth.views.login',
        {'template_name': 'nucleus/login_dialog.html'}, name='login_dialog'),
  url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page':'/'},
        name='logout'),
  url(r'^close_dialog/(?P<dialog_name>\w+)/$', 'nucleus.views.close_dialog',
        name='close_dialog'),
  url(r'', include(pagelet_patterns))
)
