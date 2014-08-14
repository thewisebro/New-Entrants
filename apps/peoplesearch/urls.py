from django.conf.urls import patterns , url
from peoplesearch.views import index

urlpatterns = patterns('',
    url(r'^$','peoplesearch.views.index'),
    url(r'^channeli_login/','peoplesearch.views.channeli_login'),
    url(r'^check_session/','peoplesearch.views.check_session'),
    url(r'^logout/','peoplesearch.views.logout_user'),
)
