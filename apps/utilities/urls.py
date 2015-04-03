from django.conf.urls import patterns, include, url

urlpatterns = patterns('utilities.views',
    (r'^profile/$','edit_profile'),
    (r'^email/$','email'),
    (r'^password/$','change_password'),
    (r'^password_firstyear/$','change_password_firstyear'),
    (r'^sessions/$','person_sessions'),
    (r'^email_auth/$','email_verify'),
    (r'^password_check/$', 'password_check'),
    (r'^forgot_password/$', 'password_reset_request'),
    (r'^password_reset/$', 'password_reset'),
    (r'^person_search/','person_search'),
)
