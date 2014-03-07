from django.conf.urls import patterns, include, url
#from django.views.generic.simple import redirect_to, direct_to_template

# haystack imports
#from haystack.forms import ModelSearchForm
#from haystack.query import SearchQuerySet
#from haystack.views import SearchView

urlpatterns = patterns('news.views',
  url(r'^$', 'html_data_extracter'),
  url(r'^home/$', 'home'),
  url(r'^international/$', 'international'),
  url(r'^national/$', 'national'),
  url(r'^sports/$', 'sports'),
  url(r'^entertainment/$', 'entertainment'),
  url(r'^item/(?P<item_id>\d+)$','news_item'),
  url(r'^search/',include('haystack.urls')),

)

'''
urlpatterns = patterns('haystack.views',
    url(r'^search/$', SearchView(
        template = "news_feeds/search.html",
        ), name = "haystack_search"),
    )
'''


