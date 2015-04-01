from django.conf.urls import *

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('mcm.views',
  (r'^mcm/$', 'mcm_submit'),
	(r'^mcm_print_pdf/$', 'mcm_print_pdf'),
  #(r'^loan_aid/$', 'loan_aid_submit'),
  #(r'^print_pdf/$', 'print_pdf'),
  (r'^data/$', 'scholarship_data_listing'),
  (r'^export/data/$', 'download_scholarship_data'),
)
