from django.conf.urls import patterns, include, url
#from django.views.generic.simple import redirect_to, direct_to_template

# haystack imports
#from haystack.forms import ModelSearchForm
#from haystack.query import SearchQuerySet
#from haystack.views import SearchView

urlpatterns = patterns('news.views',
  url(r'^extract/$', 'html_data_extracter'),
  url(r'^$', 'home'),
  url(r'^fetch/$', 'fetch_more_news'),
  #url(r'^fetch/(?P<arg>\w+)/(?P<marker>\d+)/$', 'fetch_more_news'),
  url(r'^channels_list/$', 'channels_list'),
  url(r'^international/$', 'international'),
  url(r'^national/$', 'national'),
  url(r'^sports/$', 'sports'),
  url(r'^entertainment/$', 'entertainment'),
  url(r'^technology/$', 'technology'),
  url(r'^education/$', 'education'),
  url(r'^health/$', 'health'),
  url(r'^item/(?P<item_id>\d+)/$','news_item'),
  url(r'^source/$','get_by_source'),
  url(r'^customize/$','fetch_channel_prefs'),
  url(r'^update/c_prefs/$','update_channel_prefs'),
  url(r'^search/$', 'search'),
  #url(r'^search/',include('haystack.urls')),

)

'''
urlpatterns = patterns('haystack.views',
    url(r'^search/$', SearchView(
        template = "news_feeds/search.html",
        ), name = "haystack_search"),
    )
'''


