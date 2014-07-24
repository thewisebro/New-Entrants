from django.conf.urls import patterns, include, url

urlpatterns = patterns('helpcenter.views',
  (r'^pagelet_index/$','pagelet_index'),
  (r'^feedbacks/$','feedbacks'),
  (r'^give_response$','give_response'),
  (r'^give_reply$','give_reply'),
  (r'^set_resolved$','set_resolved'),
  (r'^fetch$','fetch'),
  (r'^feedback/$','feedback'),
  (r'^login_help/$','login_help'),
  (r'^login_help/(?P<username>\w+)/$','login_help'),
)
