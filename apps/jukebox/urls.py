from django.conf.urls import patterns, include, url
from jukebox.views import *

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'channeli.views.home', name='home'),
    # url(r'^channeli/', include('channeli.foo.urls')),


    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^search/', SearchView.as_view(), name='search'),
)
