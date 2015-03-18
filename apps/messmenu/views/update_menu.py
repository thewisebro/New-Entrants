# python imports
import os
import pdb
import math
import logging, traceback
import datetime

# django imports
from django.db.models import Q
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.http import Http404
from django.core.exceptions import PermissionDenied
from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from django.template.context import RequestContext
from django.contrib.auth import logout as do_logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.context_processors import csrf
from django.contrib import messages

# models
from messmenu.models import Menu

# local imports
from messmenu.utils.views_common import add_common_functionality
from api.model_constants import BHAWAN_CHOICES
from messmenu.utils.utils import get_monday_date, get_person, is_menu_filled
from messmenu.constants import weeks_to_show

root = os.getenv("HOME")

## 'bhawan' refers to bhawan code
@login_required
@user_passes_test(lambda user: user.groups.filter(name = 'Mess Secy').exists())
def index(request, bhawan, week = 0):
  #pdb.set_trace()
  logger = logging.getLogger(__name__)
  fixed_params = add_common_functionality()
  
  week = int(week)
  if week < -2 or week > 2:
    raise Http404
  current_date = get_monday_date(0)
  ## date contains date of monday of the requested week
  if request.method == 'POST':
    bhawan = request.POST.get('bhawan', None)
    date_str = request.POST.get('date', None)
    date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
    if not(bhawan and date) or date < current_date:
      raise Http404
    try:
      Menu.save_menu(request.POST, bhawan, date)
    except:
      logger.error(traceback.format_exc())
      messages.error(request, 'Menu could not be saved. ' +
                     'Try again or contact IMG')
    else:
      return HttpResponseRedirect(reverse('display_menu',
                                          args = (bhawan, week)))

  date = current_date + datetime.timedelta(weeks = week)
  if date < current_date:
    raise Http404
  bhawans = dict(BHAWAN_CHOICES)
  try:
    request.user.person = get_person(request.user)
  except:
    return HttpResponseRedirect('/')
  try:
    if bhawan != request.user.person.bhawan:
      raise
  except:
    if request.user.person and not request.user.person.bhawan:
      ## flash session message
      pass
    raise PermissionDenied
  request.user.person.bhawan_name = bhawans.get(bhawan, '')
  try:
    week_iter = 0
    while week_iter >= -weeks_to_show:
      if is_menu_filled(week + week_iter):
        break
      week_iter -= 1
      
    if week_iter >= -weeks_to_show:
      last_filled_week = week_iter
    else:
      last_filled_week = 0
      
    date += datetime.timedelta(days = last_filled_week * 7)
    menu = get_list_or_404(Menu.objects.all(),
                            bhawan = bhawan,
                            date__gte = date,
                            date__lte = date + datetime.timedelta(days = 6)
           )
    date -= datetime.timedelta(days = last_filled_week * 7)
  except:
    logger.error(traceback.format_exc())
    raise Http404
    
  params_dict = {
    'menu': menu,
    'date': date,
    'date_str': str(date),
    'current_date': current_date,
    'bhawan': bhawan,
    'week': week,
    'bhawans': bhawans,
    'last_filled_week': last_filled_week,
  }
  params_dict.update(csrf(request))
  params_dict.update(fixed_params)

  return render_to_response('messmenu/update_menu.html',
                            params_dict,
                            context_instance = RequestContext(request))
