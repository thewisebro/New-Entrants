from django.conf.urls import patterns, url

from lectut import views

urlpatterns = patterns('',
        url(r'^$', views.tester, name='tester'),
        url(r'^disp/$', views.dispbatch, name='dispbatch'),
        url(r'^disp/(?P<batch_id>\w+)/$', views.coursepage, name='coursepage'),
        url(r'^disp/download/(?P<file_id>\w+)/$', views.download_file, name='download_file'),
        url(r'^disp/delete/(?P<file_id>\w+)/$', views.delete, name='delete'),
#       url(r'^upload/$', views.upload, name='upload'),
#  url(r'^(?P<user>[\d]+)/$', views.dispbatch, name='dispbatch'),
        url(r'^login/$','django.contrib.auth.views.login' , {'template_name':'lectut/login.html'}),
         url(r'^logout/$','django.contrib.auth.views.logout' , {'next_page':'/lectut/login'}),
    )
