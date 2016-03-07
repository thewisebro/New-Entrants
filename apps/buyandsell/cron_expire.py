from buyandsell.models import *
from datetime import datetime
from notifications.models import Notification
from feeds.models import *
from django.contrib.contenttypes.models import ContentType

def move_to_expire():
  sell_queryset = SaleItems.items.filter(is_active=True, expiry_date__lte = datetime.today().date())
  for item in sell_queryset:
    item.is_active=False
    item.save()
    c_type = ContentType.objects.get_for_model(SaleItems)
    try:
      f = Feed.objects.get(app = 'buyandsell',instance_type = c_type , instance_id = item.pk)
      f.delete()
    except:
      pass
    users = [item.user]
    notif_text = "Your item " + item.item_name + "has expired! You can reactivate it in your accounts page"
    url = "/buyandsell/my-account"
    Notification.save_notification("buyandsell" , notif_text , url,users,item)



  request_queryset = RequestedItems.items.filter(is_active=True, expiry_date__lte = datetime.today().date())
  for item in request_queryset:
    item.is_active=False
    item.save()
    c_type = ContentType.objects.get_for_model(RequestedItems)
    try:
      f = Feed.objects.get(app = 'buyandsell',instance_type = c_type , instance_id = item.pk)
      f.delete()
    except:
      pass
    users = [item.user]
    notif_text = "Your request " + item.item_name + "has expired! You can reactivate it in your accounts page"
    url = "/buyandsell/my-account"
    Notification.save_notification("buyandsell" , notif_text , url,users,item)

