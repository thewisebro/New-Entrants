from django.conf.urls import patterns, url

from lectut import views

urlpatterns = patterns('',
        url(r'^$', views.dispbatch, name='dispbatch'),
        url(r'^ajax/courses/(?P<batch_id>\w+)/$', views.coursepage, name='coursepage'),
        url(r'^ajax/(?P<batch_id>\w+)/upload/$', views.uploadedFile, name='uploadedFile'),
        url(r'^ajax/members/(?P<batch_id>\w+)/$', views.batchMembers, name='batchMembers'),
        url(r'^ajax/files/(?P<batch_id>\w+)/$', views.get_files, name='get_files'),
        url(r'^ajax/(?P<batch_id>\w+)/feed/(?P<post_id>\w+)/$', views.get_post, name='get_post'),

        url(r'^ajax/download/(?P<file_id>\w+)/$', views.download_file, name='download_file'),
        url(r'^disp/myuploads/(?P<batch_id>\w+)/$', views.useruploads, name='useruploads'),
        url(r'^disp/mydownloads/(?P<batch_id>\w+)/$', views.userdownloads, name='userdownloads'),
        url(r'^ajax/deleteFile/(?P<file_id>\w+)/$', views.deleteFile, name='deleteFile'),
        url(r'^ajax/deletePost/(?P<post_id>\w+)/$', views.deletePost, name='deletePost'),

        url(r'^ajax/createevent/$', views.createReminder, name='createReminder'),
        url(r'^ajax/search/$', views.search, name='search'),
        url(r'^ajax/events/$', views.getReminder, name='getReminder'),

        url(r'^login/$','django.contrib.auth.views.login' , {'template_name':'lectut/login.html'}),
        url(r'^logout/$','django.contrib.auth.views.logout' , {'next_page':'/lectut/login'}),
    )
