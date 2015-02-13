from core import models
from nucleus.models import User
from api import model_constants as MC
from buyandsell.constants import *
from moderation.models import Reportable
from django.conf import settings
MEDIA_ROOT = settings.MEDIA_ROOT

class BuySellCategory(models.Model):
  watch_users = models.ManyToManyField(User,blank=True)
  main_category = models.CharField(max_length=20)
  name = models.CharField(max_length=100)
  code = models.CharField(max_length=100, unique=True)
  def __unicode__(self):
    return str(self.name)

class SaleItems(Reportable, models.Model):
  user = models.ForeignKey(User)
  item_name = models.CharField(max_length = MC.TEXT_LENGTH)
  cost = models.IntegerField(max_length = MC.CODE_LENGTH)
  status = models.CharField(max_length = MC.TEXT_LENGTH, choices=STATUS)
  detail = models.TextField()
  contact = models.CharField(max_length = MC.CODE_LENGTH)
  post_date = models.DateField() # redundant because of datetime_created field. Kept to avoid changes
  days_till_expiry = models.IntegerField(max_length = MAX_NO_OF_DAYS, choices=EXPIRY)
  expiry_date = models.DateField()
  email = models.EmailField()
  category = models.ForeignKey(BuySellCategory)
  item_image = models.ImageField(upload_to='buyandsell/images', default='../static/images/buysell/default.png', blank=True)
  show_contact=models.BooleanField(default=True)
  is_active=models.BooleanField(default=True)
  def __unicode__ (self):
    return str(self.item_name)

class RequestedItems(Reportable, models.Model):
  user = models.ForeignKey(User)
  item_name = models.CharField(max_length = MC.TEXT_LENGTH)
  condition = models.CharField(max_length = MC.TEXT_LENGTH, choices=STATUS)
  price_upper = models.IntegerField(max_length = MC.CODE_LENGTH)
  price_lower = models.IntegerField(max_length = MC.CODE_LENGTH, blank= True, default=0)
  post_date = models.DateField()
  days_till_expiry = models.IntegerField(max_length = MAX_NO_OF_DAYS, choices=EXPIRY)
  expiry_date = models.DateField()
  contact = models.CharField(max_length = MC.CODE_LENGTH)
  email = models.EmailField()
  category=models.ForeignKey(BuySellCategory)
  show_contact=models.BooleanField(default=True)
  is_active=models.BooleanField(default=True)
  def __unicode__(self):
    return str(self.item_name)

class BuyMails(models.Model):
  item=models.ForeignKey(SaleItems)
  by_user=models.ForeignKey(User)
  def __unicode__(self):
    return str(self.item)

class RequestMails(models.Model):
  item=models.ForeignKey(RequestedItems)
  by_user=models.ForeignKey(User)
  def __unicode__(self):
    return str(self.item)

class SuccessfulTransaction(models.Model):
  seller=models.ForeignKey(User,related_name='suc_trans_seller')
  buyer=models.ForeignKey(User,related_name='suc_trans_buyer')
  sell_item=models.OneToOneField(SaleItems,blank=True)
  request_item=models.OneToOneField(RequestedItems,blank=True)
  is_requested=models.BooleanField(default=False) #this is to determine whose object is to be made SuccessfulTransaction for sell or request
  trasaction_date=models.DateField()
  feedback=models.TextField()

class ShowContact(models.Model):
  user=models.OneToOneField(User)
  contact_shown=models.BooleanField(default=True)  
