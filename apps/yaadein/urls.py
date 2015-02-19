
from django.conf.urls import url

from yaadein.views import *

urlpatterns = [
#   url(r'^$', index, name='index'),
    url(r'^tag/(?P<slug>[\w]+)/$',CORS_allow(TagIndexView.as_view()), name='tagged'),
    url(r'^abc/$',person_search,name='person'),
    url(r'^post/(?P<wall_user>[\w]+)/$', post , name='post'),
    url(r'^cover/upload/$', coverpic_upload, name='cover_upload'),
    url(r'^user/(?P<enrno>[\w]+)/$',index, name='tagged_user'),
    ]

