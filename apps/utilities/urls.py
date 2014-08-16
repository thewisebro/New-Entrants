from django.conf.urls import patterns, include, url

urlpatterns = patterns('utilities.views',
    (r'^profile/$','edit_profile'),
)
