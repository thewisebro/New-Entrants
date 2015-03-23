
from django.conf.urls import url

from yaadein.views import *

urlpatterns = [
#   url(r'^$', index, name='index'),
    url(r'^tag/(?P<slug>[\w]+)/$',hashtag, name='tagged'),
    url(r'^search/(?P<id>[\w]+)/$',search,name='person'),
    url(r'^post/(?P<wall_user>[\w]+)/$', post , name='post'),
    url(r'^cover/upload/$', coverpic_upload, name='cover_upload'),
    url(r'^user/(?P<enrno>[\w]+)/$',index, name='tagged_user'),
    url(r'^home/$',homePage, name='home'),
    url(r'^post_disp/(?P<pk>[\w]+)/$',post_display, name='display_post'),
    url(r'^delete/(?P<id>[\w]+)/$', delete, name='delete_post'),
    url(r'^private/(?P<id>[\w]+)/$',private_posts, name='private_post'),
    url(r'^trending/$',trending,name='trending_users'),
    url(r'^spot/(?P<name>[\w]+)/$', spot_page, name='spots'),
    url(r'^search_spot/$',spot_search,name='spots'),
    url(r'^users/$',all_users,name='users'),
    ]

