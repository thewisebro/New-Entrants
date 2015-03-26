from django.conf.urls import patterns, include, url

urlpatterns = patterns('utilities.views',
    (r'^profile/$','edit_profile'),
    (r'^email/$','email'),
    (r'^password/$','change_password'),
    (r'^password_firstyear/$','change_password_firstyear'),
    (r'^sessions/$','person_sessions'),
    (r'^person_search/','person_search'),
)
