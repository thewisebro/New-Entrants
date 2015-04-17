from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages

def handle_exc(e, request, text=None):
  print 'Exception: ' + str(e)
  if text:
    messages.error(request, text)
  else:
    messages.error(request, 'Unknown error has occured. Please try again later. The issue has beeen reported.')
  return HttpResponseRedirect(reverse('facapp.views.index'))
