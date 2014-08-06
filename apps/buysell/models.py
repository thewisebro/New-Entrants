from core import models
from nucleus.models import User
from api import model_constants as MC
from buysell.constants import *
from settings import MEDIA_ROOT

class ItemsForSale(models.Model):
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
  category = models.CharField(max_length = MC.CODE_LENGTH, choices=CATEGORY)
  sub_category = models.CharField(max_length = MC.CODE_LENGTH, choices=EMPTY)
  item_image = models.ImageField(upload_to='buysell/images', default='../static/images/buysell/default.png', blank=True)
  def __unicode__ (self):
    return str(self.item_name)

class ItemsRequested(models.Model):
  user = models.ForeignKey(User)
  item_name = models.CharField(max_length = MC.TEXT_LENGTH)
  condition = models.CharField(max_length = MC.TEXT_LENGTH, choices=STATUS)
  price_upper = models.IntegerField(max_length = MC.CODE_LENGTH)
  price_lower = models.IntegerField(max_length = MC.CODE_LENGTH, blank= True, default=0)
  post_date = models.DateField()
  expiry_date = models.DateField()
  contact = models.CharField(max_length = MC.CODE_LENGTH)
  email = models.EmailField()
  def __unicode__(self):
    return str(self.item_name)

class BuyMailsSent(models.Model):
  item=models.ForeignKey(ItemsForSale)
  by_user=models.ForeignKey(User)
  def __unicode__(self):
    return str(self.item)

class RequestMailsSent(models.Model):
  item=models.ForeignKey(ItemsRequested)
  by_user=models.ForeignKey(User)
  def __unicode__(self):
    return str(self.item)

