from django.conf.urls import patterns, url

urlpatterns = patterns('forum.views',
  url(r'^ask_question/$', 'ask_question', name='ask_question'),
  url(r'^fetch_questions/$', 'fetch_questions', name='fetch_questions'),
  url(r'^fetch_question/$', 'fetch_question', name='fetch_question'),
  url(r'^add_answer/$','add_answer',name='add_answer'),
  url(r'^fetch_answer/$','fetch_answer',name='fetch_answer'),
  url(r'^follow_question/$','follow_question',name='follow_question')
)
