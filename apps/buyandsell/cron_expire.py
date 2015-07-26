from buyandsell.models import *
from datetime import datetime

def move_to_expire():
  sell_queryset = SaleItems.objects.filter(is_active=True, expiry_date__lte = datetime.today().date())
  for item in sell_queryset:
    item.is_active=False
    item.save()
  request_queryset = RequestedItems.objects.filter(is_active=True, expiry_date__lte = datetime.today().date())
  for item in request_queryset:
    item.is_active=False
    item.save()
