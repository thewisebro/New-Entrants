# python imports
import pdb
import logging, traceback
import datetime

# django imports
from django.contrib.auth.decorators import login_required

# models
from messmenu.models import Menu

# local imports
from api.model_constants import BHAWAN_CHOICES
from messmenu.utils.utils import get_monday_date, get_person


@login_required
def add(request):
  print 'adding comment'
  return 

  
@login_required
def delete(request):
  print 'removing comment'
  return 

