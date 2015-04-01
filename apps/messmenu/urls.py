from django.conf.urls import patterns, url
#from django.contrib.comments.models import FreeComment

urlpatterns = patterns('messmenu.views',
	url(r'^$', 'display_menu.index', name = 'display_menu_default'),
	url(r'^(?P<bhawan>\w+)/(?P<week>[-]?\d)$', 'display_menu.index', 
      name = 'display_menu'),
	url(r'^update_menu/(?P<bhawan>\w+)/(?P<week>[-]?\d)$', 'update_menu.index',
      name = 'update_menu'),
  url(r'^(?P<pdf>\w+)/(?P<bhawan>\w+)/(?P<week>[-]?\d)$', 'display_menu.index',
      name = 'generate_pdf'),
  url(r'^todays_menu/$', 'display_menu.todays_menu'),
  url(r'^feedback/$', 'feedback.feedback'),
)

"""urlpatterns += patterns('messmenu',
	url(r'^update/?$', 'utils.scripts.update_data.index'),
)"""

urlpatterns += patterns('messmenu.ajax',
  url(r'^save_menu$', 'save_menu.index', name = 'save_menu'),
  url(r'^add_comment$', 'user_comments.add', name = 'add_user_comment'),
  url(r'^delete_comment$', 'user_comments.delete', name = 'delete_user_comment'),
)

