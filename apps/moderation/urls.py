from django.conf.urls import patterns, include, url

urlpatterns = patterns('moderation.views',
    (r'^submit_report/$', 'submit_report'),
    (r'^report_info/$', 'report_info'),
)

