from django.conf.urls import patterns, include, url

urlpatterns = patterns('feeds.views',
    (r'^fetch$','fetch')
)
