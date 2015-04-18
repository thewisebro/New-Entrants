from notices.models import *
from datetime import datetime

def move_to_expire():
  print "entered move_to_expire at date : ", datetime.today().date()
  queryset = Notice.objects.filter(expired_status=False, expire_date__lt = datetime.today().date())
  for notice in queryset:
    notice.expired_status=True
    notice.save()
    print "notice with id : " + str(notice.id) + "has expired"
