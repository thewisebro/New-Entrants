from nucleus.models import *
from buyandsell.models import *
from django.utils import timezone
from buysell.models import *
from datetime import datetime
from django.conf import settings
MEDIA_ROOT = settings.MEDIA_ROOT
import os.path


def move_requests():
  items_to_move = ItemsRequested.objects.all()
  for item in items_to_move:
    new_item = RequestedItems()
    new_item.user = item.user
    new_item.item_name = item.item_name
    new_item.price_upper = item.price_upper
    new_item.post_date = item.post_date
    new_item.expiry_date = item.expiry_date
    new_item.days_till_expiry = (item.expiry_date-item.post_date).days
    new_item.contact = item.contact
    new_item.email = item.email
    new_item.category = BuySellCategory.objects.get(pk = 11)
    if timezone.now().date() > new_item.expiry_date:
      new_item.is_active = False
    new_item.save()
    mapped_entry = OldRequestMap(request_id = item.pk ,item= new_item)
    mapped_entry.save()


def move_mails():
  requests_to_move = ItemsRequested.objects.filter()
  sellitems_to_move = ItemsForSale.objects.filter()
  for request in requests_to_move:
   mails = RequestMailsSent.objects.filter(item = request)

   for mail in mails:
     new_mail = RequestMails()
     new_mail.item = request
     new_mail.by_user = mail.by_user
     new_mail.save()

  for sell in sellitems_to_move:
    mails = BuyMailsSent.objects.filter(item = sell)
    new_sell =SaleItems.objects.filter(item_name = sell.item_name,cost = sell.cost,detail = sell.detail,contact = sell.contact)
# print len(new_sell)
    new_sell =SaleItems.objects.filter(item_name = sell.item_name)[0]
    for mail in mails:
      new_mail = BuyMails()
      new_mail.item = new_sell
      new_mail.by_user = mail.by_user
      new_mail.save()

def move_sellitems():
  items_to_move = ItemsForSale.objects.all()
  for item in items_to_move:
    new_item = SaleItems()
    new_item.user = item.user
    new_item.cost = item.cost
    new_item.item_name = item.item_name
    new_item.detail = item.detail
    new_item.contact = item.contact
    new_item.post_date = item.post_date
    new_item.days_till_expiry = item.days_till_expiry
    new_item.expiry_date = item.expiry_date
    new_item.email = item.email

    sc = item.sub_category
    mc = item.category

    if sc == 'LP':
       new_item.category = BuySellCategory.objects.get(pk = 2 )

    elif sc == 'MO':
       new_item.category = BuySellCategory.objects.get(pk = 6 )

    elif sc == 'OT':
       if mc == 'EL':
         new_item.category = BuySellCategory.objects.get(pk = 5 )
       elif mc == 'BK':
         new_item.category = BuySellCategory.objects.get(pk = 9 )
       elif mc == 'MS':
         new_item.category = BuySellCategory.objects.get(pk = 11)

    elif sc == 'ED':
       new_item.category = BuySellCategory.objects.get(pk = 7 )

    elif sc == 'CS':
       new_item.category = BuySellCategory.objects.get(pk = 8 )

    elif sc == 'FC':
       new_item.category = BuySellCategory.objects.get(pk = 3 )

    elif sc == 'TR':
       new_item.category = BuySellCategory.objects.get(pk = 4 )

    elif sc == 'BC':
       new_item.category = BuySellCategory.objects.get(pk = 10 )\

    if timezone.now().date() > new_item.expiry_date:
      new_item.is_active = False

    new_item.save()
    new_pic = ItemPic(item = new_item)
    new_pic.save()
    file_url = os.path.join(MEDIA_ROOT , item.item_image.url)
    if file_url !=  '/static/images/buysell/default.png':
#  print file_url
      try:
        name = item.item_image.name
        new_item.itempic.pic.save(name,item.item_image,save=True)
        new_item.save()  #for notification
      except:
        pass
    mapped_entry = OldBuyMap(buy_id = item.pk ,item= new_item)
    mapped_entry.save()
    

















