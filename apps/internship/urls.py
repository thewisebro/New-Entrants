from django.conf.urls import *
from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required

urlpatterns = patterns ('internship.views',
  (r'^$', 'index'),
  (r'^company/(?P<company_id>\w+)/info/$', 'company_info'),
  (r'^resume/$', 'resume'),
  (r'^resume/(?P<enrollment_no>\d+)/$', 'resume_to_verify'),
  (r'^company/(?P<company_id>\d+)/opento/$','company_open_to'),
  (r'^FAQ/$', login_required(TemplateView.as_view(template_name='internship/FAQ.html'))),
)


urlpatterns += patterns ('internship.views_student',     ### 3 url solved
  (r'^company/list/$', 'company_list'),
  (r'^company/(?P<company_id>\w+)/apply/$', 'apply'),
  (r'^company/(?P<company_id>\w+)/withdraw/$', 'withdraw'),
  (r'^company/(?P<company_id>\w+)/resume/$', 'submitted_resume'),
#  (r'^priority/$', 'set_priority'),
)

urlpatterns += patterns ('internship.views_notice',
  (r'^notices/$', 'notice_list'),
  (r'^notice/(?P<notice_id>\d+)/$', 'notice_view'),
  #(r'^notices/archive/$', 'notice_archive'),
  # Notice Admin urls
  (r'^notice/add/$', 'notice_add'),
  (r'^notices/admin/$', 'notice_list_admin'),
  (r'^notice/(?P<notice_id>\w+)/edit/$', 'notice_edit'),
  (r'^notice/(?P<notice_id>\w+)/delete/$', 'notice_delete'),
)

urlpatterns += patterns ('internship.views_results',
  # Result viewing urls
  (r'^results/company/$','results_company_list'),
  (r'^results/(?P<year>\d{4})/company/$','results_company_list'),
  #(r'^results/company/(?P<company_name>[\w\ ]+)/$','company_results'),
  (r'^results/company/(?P<company_id>\d+)/$','company_results'),
  #(r'^results/(?P<year>\d{4})/company/(?P<company_name>[\w\ \.\,\-\']+)/$','company_results'),
  (r'^results/(?P<year>\d{4})/company/(?P<company_id>\d+)/$','company_results'),
  (r'^results/branch/$','results_discipline_list'),
  (r'^results/(?P<year>\d{4})/branch/$','results_discipline_list'),
  (r'^results/branch/(?P<discipline_name>[\w\ ]+)/$','branch_results'),
  (r'^results/(?P<year>\d{4})/branch/(?P<discipline_name>[\w\ ]+)/$','branch_results'),
  (r'^results/(?P<year>\d{4})/branch/(?P<discipline_name>[\w\ ]+)/company/$','branch_results_company'),
  (r'^results/company/(?P<company_id>\d+)/declare/$', 'declare_result'),
  (r'^results/company/(?P<company_id>\d+)/drop/$', 'drop_results'),
  (r'^results/company/(?P<company_id>\d+)/insert/(?P<branch_code>\w+)/$', 'insert_result'),
  (r'^results/company/(?P<company_id>\d+)/insert/$', 'insert_result'),
)

urlpatterns += patterns('internship.views_admin',  #### First URL solved
  #Admin URLS
  (r'^company/$', 'company_list_admin'),
  (r'^company/add/$', 'company_add'),
  (r'^branch/$', 'branch_details'),
  (r'^branch/(?P<branch_code>\w+)/$', 'branch_details'),
  (r'^company/(?P<company_id>\w+)/delete/$', 'company_delete'),
  (r'^company/(?P<company_id>\w+)/$', 'company_edit'),
  (r'^company/(?P<company_id>\d+)/applications/finalize/$', 'applications_to_company'),
  (r'^company/(?P<company_id>\d+)/applications/unfinalize/$', 'unfinalize'),
  (r'^company/(?P<company_id>\d+)/applications/unfinalize/(?P<degree>\w+)/$', 'unfinalize'),
  (r'^company/(?P<company_id>\d+)/applications/selected_students/$', 'selected_students'),
  (r'^company/(?P<company_id>\d+)/applications/selected_resumes/$', 'resume_archive'),
)

urlpatterns += patterns('internship.views_forum',
  # Forum urls
  (r'^forum/$', 'forum_post'),
  (r'^forum/(?P<forum_type>[T|P])/$', 'forum'),
  (r'^forum/(?P<forum_type>[T|P])/(?P<page_no>\d+)/$', 'forum'),
)  
  
urlpatterns += patterns('internship.views_feedback',
  # Feedback
  (r'^feedback/$', 'feedback_company_list'),
  (r'^feedback/(?P<year>\d{4})/$', 'feedback_company_list'),
  (r'^feedback/(?P<year>\d{4})/company/(?P<company_name>[\w\ ]+)/$', 'company_feedback'),
  (r'^feedback/add/$', 'feedback'),
  (r'^feedback/pdf/(?P<feedback_id>\d+)/$', 'feedback_as_pdf'), 
  (r'^feedback/company/(?P<company_name>[\w\ ]+)/$', 'feedback_company_as_pdf'),
)
