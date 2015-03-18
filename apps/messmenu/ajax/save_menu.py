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
def index(request):
  #logger = logging.getLogger(__name__)
  #pdb.set_trace()
  current_date = get_monday_date(0)
  ## current_date contains date of monday of the current week
  if request.method == 'POST':
    bhawan = request.POST.get('bhawan', None)
    date_str = request.POST.get('date', None)
    try:
      date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
    except:
      return ErrorResponse(error_msg = 'date improperly set')
    if not(bhawan and date) or date < current_date:
      #logger.warning('bhawan/date not set or improperly set')
      return ErrorResponse(error_msg = 'There was some error in processing')
    try:
      Menu.save_menu(request.POST, bhawan, date)
      print '111'
      try:
        return SuccessResponse()
      except:
        print traceback.format_exc()
    except:
      return ErrorResponse(error_msg = 'database error')
  return ErrorResponse(error_msg = 'There was some error in processing')
