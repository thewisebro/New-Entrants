from django.conf.urls import patterns , url
from peoplesearch.views import index

urlpatterns = patterns('',
    url(r'^$','peoplesearch.views.index'),
)
