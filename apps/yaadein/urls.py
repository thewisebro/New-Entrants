
from django.conf.urls import url

from yaadein.views import *

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^tag/(?P<slug>[\w]+)/$',TagIndexView.as_view(), name='tagged'),
    url(r'^abc$',person_search,name='person'),
    url(r'^user/(?P<name>[\w]+)/$',tag_user.as_view(), name='tagged_user'),

    ]

