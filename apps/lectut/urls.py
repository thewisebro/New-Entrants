from django.conf.urls import patterns, url

from lectut import views

urlpatterns = patterns('',
        url(r'^$', views.dispbatch, name='dispbatch'),
        url(r'^feeds/(?P<batch_id>\w+)/$', views.coursepage, name='coursepage'),
        url(r'^batchDetails/(?P<batch_id>\w+)/$', views.batch_data, name='batch_data'),
        url(r'^upload/(?P<batch_id>\w+)/$', views.uploadedFile, name='uploadedFile'),
        url(r'^members/(?P<batch_id>\w+)/$', views.batchMembers, name='batchMembers'),
        url(r'^files/(?P<batch_id>\w+)/$', views.get_files, name='get_files'),

        url(r'^feeds/(?P<batch_id>\w+)/(?P<post_id>\w+)/$', views.get_post, name='get_post'),
        url(r'^feeds/file/(?P<batch_id>\w+)/(?P<file_id>\w+)/$', views.get_file, name='get_file'),
        url(r'^feeds/$', views.latest_feeds, name='latest_feeds'),

        url(r'^download/(?P<file_id>\w+)/$', views.download_file, name='download_file'),
        url(r'^myuploads/(?P<batch_id>\w+)/$', views.useruploads, name='useruploads'),
        url(r'^mydownloads/(?P<batch_id>\w+)/$', views.userdownloads, name='userdownloads'),
        url(r'^deleteFile/(?P<file_id>\w+)/$', views.deleteFile, name='deleteFile'),
        url(r'^deletePost/(?P<post_id>\w+)/$', views.deletePost, name='deletePost'),

# URLS for initial regiteration of batches
        url(r'^createBatch/$', views.create_batch, name='create_batch'),
#        url(r'^joinBatch/(?P<batch_id>\w+)/$', views.join_batch, name='join_batch'),
        url(r'^batch_data_student/$', views.ini_batch_student, name='ini_batch_student'),
        url(r'^batch_data_faculty/$', views.ini_batch_faculty, name='ini_batch_faculty'),

        url(r'^createevent/$', views.createReminder, name='createReminder'),
        url(r'^search/$', views.search, name='search'),
        url(r'^joinBatch/(?P<batch_id>\w+)/$', views.join_batch, name='join_batch'),
        url(r'^leaveBatch/(?P<batch_id>\w+)/$', views.leave_batch, name='leave_batch'),
        url(r'^facultyFiles/(?P<faculty_id>\w+)/$', views.faculty_files, name='faculty_files'),

        url(r'^events/$', views.getReminder, name='getReminder'),
        url(r'^comments/(?P<post_id>\w+)/$', views.post_comments, name='post_comments'),
        url(r'^add_comment/(?P<post_id>\w+)/$', views.add_comment, name='add_comment'),

        url(r'^login/$','django.contrib.auth.views.login' , {'template_name':'lectut/login.html'}),
        url(r'^logout/$','django.contrib.auth.views.logout' , {'next_page':'/lectut/login'}),
    )
