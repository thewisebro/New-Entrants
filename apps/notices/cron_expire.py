from notices.models import *
from datetime import datetime

def move_to_expire():
  queryset = Notice.objects.filter(expired_status=False, expire_date__lt = datetime.today().date())
  for notice in queryset:
    notice.expired_status=True
    notice.save()
