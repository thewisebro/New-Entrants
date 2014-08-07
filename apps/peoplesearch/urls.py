from django.conf.urls import patterns , url
from peoplesearch.views import index

urlpatterns = patterns('',
    url(r'^$','peoplesearch.views.index'),
    url(r'^$','peoplesearch.views.channeli_login'),
    url(r'^$','peoplesearch.views.check_session'),
    url(r'^$','peoplesearch.views.logout_user'),
)
