from django.contrib.auth.decorators import login_required
from datetime import date, datetime, timedelta
from django.template import RequestContext




 @login_required
def index(request):
  user=request.user

