from django.conf.urls import patterns, url
from genforms.views import *

urlpatterns = patterns('',
        url(r'^$', 'genforms.views.libform_view', name='libform'),
)
