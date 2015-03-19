from django.conf.urls import patterns, include, url
# from django.views.generic.simple import direct_to_template

# from api.filemanager import path_end

urlpatterns = patterns('facapp.views',
    (r'^$', 'index'),
    (r'^add/(?P<model_name>\w+)/$', 'add'),
    # (r'^update/(?P<model_name>\w+)/(?P<instance_id>\d+)/$', 'update'),
    # (r'^delete/(?P<model_name>\w+)/(?P<instance_id>\d+)/$', 'delete'),
    # (r'^publish/$','publish'),
)
# urlpatterns += patterns('facapp.views_mass_mailer',
#     (r'^mass_mailer/$', 'mass_mailer'),
#     (r'^mass_mailer/choose_semester/$', 'choose_semester'),
#     (r'^mass_mailer/show_student_list/$', 'show_student_list'),
# )
# urlpatterns += patterns('facapp.views_ckeditor',
#     (r'^books_authored/$', 'books_authored'),
#     (r'^refereed_journal_papers/$', 'refereed_journal_papers'),
#     (r'^refereed_journal_papers/edit/$', 'refereed_journal_papers_edit'),
#     (r'^books_authored/edit/$', 'books_authored_edit'),
# )
# urlpatterns += patterns('facapp.views_upload',
#     (r'^upload/photo/$', 'upload_photo'),
#     (r'^upload/resume/$', 'upload_resume'),
#     (r'^websitebrowser/'+path_end, 'websitebrowser'),
#     (r'^website_page/$', 'website_page'),
#     (r'^filemanagerhelp/$', direct_to_template, {'template':'facapp/filemanagerhelp.html'}),
#     (r'^filemanager/'+path_end,'faculty_filemanager')
# )
