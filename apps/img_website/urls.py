from django.conf.urls import patterns, url, include
from img_website import views
from filemanager import path_end

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
  url(r'^admin/', include(admin.site.urls)),
  url(r'^$', views.index, name="index"),
  url(r'^login/$', 'nucleus.views.login'),
  url(r'^logout/$', 'nucleus.views.logout'),
  url(r'^about/$', views.about, name="about"),
  url(r'^contact/$', views.contact, name="contact"),
#blog urls
  url(r'^blog/$', views.post_list, name="static_blog"),
  url(r'^dynamic_blog/$', views.post_list_dynamic, name="blog"),
  url(r'^blog/search/$', views.search_post, name="search"),
  url(r'^dynamic_blog/create/$', views.create_post, name="create"),
  url(r'^dynamic_blog/(?P<slug>[\w\-\(\)\&\:\,\?\!\.]+)/update/$', views.update_post, name="update"),
  url(r'^dynamic_blog/(?P<slug>[\w\-\(\)\&\:\,\?\!\.]+)/delete/$', views.delete_post, name="delete"),
  url(r'^blog/(?P<slug>[\w\-\(\)\&\:\,\?\!\.]+)/publish_now/$', views.publish_blog_post, name="publish_now"),
  url(r'^blog/(?P<slug>[\w\-\(\)\&\:\,\?\!\.]+)/unpublish_now/$', views.unpublish_blog_post, name="unpublish_now"),
  url(r'^blog/(?P<slug>[\w\-\(\)\&\:\,\?\!\.]+)/$', views.post_detail, name="static_detail"),
  url(r'^dynamic_blog/(?P<slug>[\w\-\(\)\&\:\,\?\!\.]+)/$', views.post_detail_dynamic, name="detail"),
#work urls
  url(r'^works/$', views.work_list, name="static_works"),
  url(r'^works/page/(?P<page>\w+)/$', views.work_list, name="static_works_page"),
  url(r'^dynamic_works/$', views.work_list_dynamic, name="works"),
  url(r'^dynamic_works/create/$', views.create_work, name="create"),
  url(r'^dynamic_works/(?P<slug>[\w\-\(\)\&\:\,\?\!\.]+)/update/$', views.update_work, name="update"),
  url(r'^dynamic_works/(?P<slug>[\w\-\(\)\&\:\,\?\!\.]+)/delete/$', views.delete_work, name="delete"),
  url(r'^works/(?P<slug>[\w\-\(\)\&\:\,\?\!\.]+)/publish_now/$', views.publish_works, name="publish_now"),
  url(r'^works/(?P<slug>[\w\-\(\)\&\:\,\?\!\.]+)/unpublish_now/$', views.unpublish_works, name="unpublish_now"),
  url(r'^works/(?P<slug>[\w\-\(\)\&\:\,\?\!\.]+)/$', views.work_detail, name="static_detail"),
  url(r'^dynamic_works/(?P<slug>[\w\-\(\)\&\:\,\?\!\.]+)/$', views.work_detail_dynamic, name="detail"),
#team urls
  url(r'^team/add_member/$', views.add_member, name="addmember"),
  url(r'^team/$', views.member_list, name="memberlist"),
#edit
  url(r'^edit/$', views.edit, name="edit"),
  url(r'^browse/'+path_end, views.media, name="browse"),
#status urls
  url(r'^status/$', views.status_post_list, name="static_status_post"),
  url(r'^status_ajax/$', views.status_ajax, name="status_json"),
  url(r'^dynamic_status/$', views.status_post_list_dynamic, name="status_posts"),
  url(r'^dynamic_status/create/$', views.create_status_post, name="create"),
  url(r'^dynamic_status/(?P<pk>[0-9]+)/update/$', views.status_post_update, name="update"),
#url(r'^status/(?P<pk>[0-9]+)/$', views.status_post_detail, name="static_detail"),
#url(r'^dynamic_status/(?P<pk>[0-9]+)/$', views.status_post_detail_dynamic, name="detail"),
  url(r'^status/(?P<pk>[0-9]+)/publish_now/$', views.publish_status_post, name="publish_now"),
  url(r'^status/(?P<pk>[0-9]+)/unpublish_now/$', views.unpublish_status_post, name="unpublish_now"),

)
