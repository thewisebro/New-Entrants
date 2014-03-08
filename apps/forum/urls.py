from django.conf.urls import patterns, url

urlpatterns = patterns('forum.views',
  url(r'^ask_question/$', 'ask_question', name='ask_question'),
  url(r'^fetch_questions/$', 'fetch_questions', name='fetch_questions'),
  url(r'^fetch_question/$', 'fetch_question', name='fetch_question'),
  url(r'^add_answer/$','add_answer',name='add_answer'),
  url(r'^fetch_answer/$','fetch_answer',name='fetch_answer'),
  url(r'^follow_question/$','follow_question',name='follow_question'),
  url(r'^unfollow_question/$','unfollow_question',name='unfollow_question'),
  url(r'^remove_upvote/$','remove_upvote',name='remove_upvote'),
  url(r'^remove_downvote/$','remove_downvote',name='remove_downvote'),
  url(r'^upvote_answer/$','upvote_answer',name='upvote_answer'),
  url(r'^downvote_answer/$','downvote_answer',name='downvote_answer'),
  url(r'^fetch_tag/$','fetch_tag',name='fetch_tag'),
  url(r'^fetch_activity/$','fetch_activity',name='fetch_activity'),
  url(r'^follow_tag/$','follow_tag',name='follow_tag'),
  url(r'^unfollow_tag/$','unfollow_tag',name='unfollow_tag'),
  url(r'^search_tag/$','search_tag',name='search_tag')
)
