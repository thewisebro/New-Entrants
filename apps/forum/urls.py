from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^ask_question/', 'forum.views.ask_question', name='ask_question')
)
