from django.conf.urls import patterns, url

from lectut import views

urlpatterns = patterns('',
        url(r'^$', views.tester, name='tester'),
        url(r'^disp/$', views.dispbatch, name='dispbatch'),
        url(r'^disp/(?P<course_name>\w+)/$', views.coursepage, name='coursepage'),
        url(r'^upload/$', views.upload, name='upload'),
#  url(r'^(?P<user>[\d]+)/$', views.dispbatch, name='dispbatch'),
        url(r'^login/$','django.contrib.auth.views.login' , {'template_name':'lectut/login.html'}),
         url(r'^logout/$','django.contrib.auth.views.logout' , {'next_page':'/lectut/login'}),
    )
