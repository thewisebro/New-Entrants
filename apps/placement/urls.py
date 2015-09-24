from django.conf.urls import patterns, include, url
from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required

# HC means Hard Coded and hence the url cannot be changed
# All other urls can be modified without any problem.

urlpatterns = patterns('placement.views',
  (r'^$', 'index'),
  (r'^resume/$','resume'),
  (r'^resume_nik/$','resume_nik'),
  (r'^toggle/$','toggle'),
  (r'^scorecard/$','scorecard'),
  (r'^company/(?P<company_id>\d+)/apply/$','apply'),
  (r'^company/(?P<company_id>\d+)/withdraw/$','withdraw'),
  (r'^FAQ/$', login_required(TemplateView.as_view(template_name='placement/FAQ.html'))),
  (r'^mynewsstudio/$',login_required(TemplateView.as_view(template_name='placement/my_news_studio.html'))),
  (r'^sample/resumes/$',login_required(TemplateView.as_view(template_name='placement/samples.html'))),
# Forum urls
  (r'^forum/$', 'forum_post'),
  (r'^forum/(?P<forum_type>(T|P))/$', 'forum'),
  (r'^forum/(?P<forum_type>(T|P))/(?P<page_no>\d+)/$', 'forum'),
)

# Slots urls
urlpatterns += patterns('placement.views_slots',
                       (r'^slots/$', 'view_all_slots'),
                       (r'^slot/(?P<slot_id>\d+)/$', 'view_slot'),
                       (r'^slot/create/$', 'create_slot'),
                       (r'^slot/edit/(?P<slot_id>\d+)/$', 'edit_slot'),
                       (r'^slot/generate_xls/(?P<slot_id>\d+)/$', 'import_slot_data'),
                       (r'^company_search/','company_search'),
)

# IMG urls
urlpatterns += patterns('placement.views_img',
                       (r'^update/$','update_status'),
                       (r'^generate/(?P<company_id>\d+)/$','generate_missing_resumes'), #No link available; do it directly in emergency
                       (r'^registration/$','generate_registration_no'),
                       (r'^contact_manager/$','placement_manager_view'),
                       (r'^contact_manager/contactperson_data/$','placement_manager_contact_person_data'),
                       (r'^contact_manager/contactperson_data_export/$','placement_manager_contact_person_data_export'),
                       (r'^company_coordinator/$', 'company_coordinator_view'),
                       (r'^contact_manager/(?P<user_id>\d+)/$', 'company_coordinator_view'),
                       (r'^company_coordinator/contactperson_data/$','company_coordinator_contact_person_data'),
                       (r'^company_coordinator/contactperson_data/(?P<user_id>\d+)/$','company_coordinator_contact_person_data'),
                       (r'^company_coordinator/today/$', 'company_coordinator_today_view'),
                       (r'^company_coordinator/contactperson_data/today/$','company_coordinator_contact_person_data_today'),
                       (r'^contactmanager_manual/$','add_company_manual'),
                       (r'^contact_manager/edit/(?P<company_id>\d+)/$','edit_company_manual'),
                       (r'^contact_manager/edit/comments/(?P<company_id>\d+)/$','edit_comments'),
                       (r'^contact_manager/remove/comments/(?P<comment_id>\d+)/$','delete_comments'),
                       (r'^contact_manager/remove/(?P<company_id>\d+)/$','contactmanager_delete'),
                       (r'^contact_manager/remove_campuscontact/(?P<campuscontact_id>\d+)/$','campuscontact_delete'),
                       (r'^contact_manager/details/(?P<company_id>\d+)/$','company_details'),
                       (r'^contact_manager/assign','assign_campus_contact'),
                       (r'^contact_manager/add/$', 'add_company_coordinator'),
                       (r'^contact_manager/person_search/$', 'person_search'),
                       (r'^contact_manager/company_search/$', 'company_search'),
#                      (r'^contact_manager/generate_xls/$', 'generate_company_contact_xls'),
    )

# Admin urls
urlpatterns += patterns('placement.views_admin',
                        (r'^company/(?P<company_id>\d+)/applications/finalize/$', 'finalize'),
                        (r'^company/(?P<company_id>\d+)/applications/finalize/(?P<degree>\w+)/$', 'finalize'),
                        (r'^company/(?P<company_id>\d+)/applications/unfinalize/$', 'unfinalize'),
                        (r'^company/(?P<company_id>\d+)/applications/unfinalize/(?P<degree>\w+)/$', 'unfinalize'),
                        (r'^company/(?P<company_id>\d+)/applications/shortlist/$', 'shortlist'),
                        (r'^company/(?P<company_id>\d+)/applications/shortlist/(?P<task>(xlslist|resumes))/$', 'shortlist'),
                        (r'^company/(?P<company_id>\d+)/applications/selected_resumes/$', 'resume_archive'),
                        (r'^company/(?P<company_id>\d+)/applications/selected_students/$', 'selected_students'),
                        (r'^cpt/$', 'cpt'),
                        (r'^cpt/(?P<year>\d{4})/$', 'cpt'),
                        (r'^cpt/add/$', 'cpt_add'),
                        (r'^cpt/member/(?P<member_id>\d+)/$', 'cpt_edit'),
                        (r'^cpt/delete/(?P<member_id>\d+)/$', 'cpt_delete'),
                        (r'^notices/$','notices'),
                        (r'^notices/(?P<page_no>\d+)/$','notices'),
                        (r'^notices/upload/$','notice_upload'),
                        (r'^branch/$', 'branch_details'),
                        (r'^branch/(?P<branch_code>\w+)/$', 'branch_details'),
                        (r'^branch/(?P<branch_code>\w+)/xls/$', 'branch_details_xls'),
                        (r'^secondround/$', 'second_round'),
                        (r'^downloads/$', 'downloads'),
                        (r'^test/$', 'test'),
                        (r'^insert_shortlist/$', 'insert_shortlist'),
                        (r'^plac_person_search/$','plac_person_search'),
                        (r'^ppo_rejection/$','ppo_rejection'),
                        (r'^ppo_rejection/remove/(?P<ppo_id>\d+)/$','ppo_rejection_delete'),
                       )

# Company urls
urlpatterns += patterns('placement.views_company',
                        (r'^company/list/$','list'),
#                        (r'^workshop_registration/$', 'workshop_registration'),
#                        (r'^workshop_registration_details/$', 'workshop_registration_details'),
                       (r'^workshop_registration_export/$', 'workshop_registration_export'),
#                       (r'^workshop_priority/$', 'set_workshop_priority'),
                        (r'^company/(?P<company_id>\d+)/info/$','info'),
                        (r'^company/(?P<company_id>\d+)/opento/$','open_to'),
                        (r'^company/$', 'admin_list'),
                        (r'^company/add/$', 'add'),
                        (r'^company/(?P<company_id>\d+)/$', 'edit'),
                        (r'^company/(?P<company_id>\d+)/delete/$', 'delete'),
                        )

# Feedback urls
urlpatterns += patterns('placement.views_feedback',
                        (r'^feedback/$', 'index'),
                        (r'^feedback/(?P<year>\d{4})/$', 'index'),
                        (r'^feedback/company/(?P<company_id>\d+)/$', 'company'),
                        (r'^feedback/add/$', 'fill'),
                        (r'^feedback/pdf/(?P<feedback_id>\d+)/$', 'as_pdf'),
                        )

# Student profile urls
urlpatterns += patterns('placement.views_profiles',
                        (r'^photo/$', 'photo'),
                        (r'^personal_information/$', 'personal_information'),
                        (r'^contact/$', 'contact'),
                        (r'^educational_details/$', 'educational_details'),
                        (r'^placement_information/$', 'placement_information'),
                        (r'^editset/(?P<model_name>\w+)/$', 'editset'),
                        )

# Result urls
urlpatterns += patterns('placement.views_results',
                        (r'^results/company/$','company_list'),
                        (r'^results/(?P<year>\d{4})/company/$','company_list'),
                        (r'^results/company/(?P<company_id>\d+)/$','company'),
                        (r'^results/(?P<year>\d{4})/company/(?P<company_id>\d+)/$','company'),
                        (r'^results/branch/$','discipline_list'),
                        (r'^results/(?P<year>\d{4})/branch/$','discipline_list'),
                        (r'^results/branch/(?P<branch_code>[\w\ ]+)/$','branch'),
                        (r'^results/(?P<year>\d{4})/branch/(?P<branch_code>[\w\ ]+)/$','branch'),
                        (r'^results/(?P<year>\d{4})/branch/(?P<branch_code>[\w\ ]+)/company/$','branch_company'),
                        (r'^results/company/(?P<company_id>\d+)/declare/$', 'declare'),
                        (r'^results/company/(?P<company_id>\d+)/insert/$', 'insert'),
                        (r'^results/company/(?P<company_id>\d+)/insert/(?P<branch_code>\w+)/$', 'insert'),
                        (r'^results/company/(?P<company_id>\d+)/drop/$', 'drop'),
                        (r'^results/department/$', 'department'),
                        (r'^results/(?P<year>\d{4})/department/$', 'department'),
                        (r'^results/department/(?P<department_id>\D+)/$', 'department'),
                        (r'^results/(?P<year>\d{4})/department/(?P<department_id>\w+)/$', 'department'),
                        (r'^results/department/(?P<department_id>\D+)/(?P<degree>[\w.]+)/$', 'department'),
                        (r'^results/(?P<year>\d{4})/department/(?P<department_id>\w+)/(?P<degree>[\w.]+)/$', 'department'),
                        )

# Verification urls
urlpatterns += patterns('placement.views_verify',
                        (r'^verify/$','index'),
                        (r'^changestatus/(?P<enrollment_no>\d+)/$','change_status'),                            #HC
                        (r'^changestatus/(?P<enrollment_no>\d+)/(?P<status>\w+)/$','change_status'),            #HC
                        (r'^changedebarstatus/(?P<enrollment_no>\d+)/(?P<status>\w+)/$','change_debar_status'), #HC
                        (r'^verify/branch/$','branch_list'),
                        (r'^verify/department/$','department_list'),
                        (r'^verify/unverified_list/$','unverified_list'),
                        (r'^verify/resume/(?P<enrollment_no>\d+)/$','resume'),                                  #HC
                        (r'^verify/scorecard/(?P<enrollment_no>\d+)/$','scorecard'),                            #HC
                        (r"^(?P<task>(verify|unverify|unlock|reverify|verified))/(?P<branch_code>\w+)/$",'verify'),
                        (r"^(?P<task>(verify|unverify|unlock|reverify|verified))/department/(?P<department_code>\w+)/$",'verify_department'),
                        )


# media urls
urlpatterns += patterns('placement.media',
                        (r'^media/photo/$', 'photo'),
                        (r'^media/brochures/(?P<company_id>\w+)/$', 'brochures'),
                        (r'^media/company/(?P<company_id>\w+)/resume/$','submitted_resume'),
                        (r'^media/results/institute/sectorwise/$', 'institute_results_sectorwise'),
                        (r'^media/results/institute/companywise/$', 'institute_results_companywise'),
                        (r'^media/results/institute/branchwise/$', 'institute_results_branchwise'),
                        (r'^media/results/institute/$', 'institute_results'),
                        )
