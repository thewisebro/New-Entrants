from django.core.urlresolvers import reverse
from django.contrib import messages
from django.http import HttpResponseRedirect, Http404

import logging, os
l = logging.getLogger('channel-i_logger')

##########################################################################
# This module is for utility functions, no logs should be generated here #
# for normal operations. Error and important logs can be made by these   #
# functions but info logs must be handled in the calling function only.  #
##########################################################################

def handle_exc(e, request, text=None):
  l.error(e)
  if isinstance(e, Http404) :
    # TODO : do whatever you wanna do here, you may display a message or a 404 page
    raise Http404
  if text:
    messages.error(request, text)
  else:
    messages.error(request, 'Unknown error has occured. Please try again later. The issue has beeen reported.')
  return HttpResponseRedirect(reverse('internship.views.index'))

