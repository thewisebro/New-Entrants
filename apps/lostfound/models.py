from core import models
from nucleus.models import User
from api import model_constants as MC
from lostfound.constants import *
from datetime import date

# Create your models here.
class LostItems(models.Model):
  user = models.ForeignKey(User)
  item_lost = models.CharField(max_length = MC.TEXT_LENGTH)
  category = models.CharField(max_length = MC.TEXT_LENGTH, choices=CATEGORY)
  place = models.CharField(max_length = MC.TEXT_LENGTH)
  status = models.CharField(max_length = MC.TEXT_LENGTH)
  other_details = models.TextField(blank=True)
  contact = models.CharField(max_length = 20)   # see facapp.models for more
  address = models.CharField(max_length = MC.TEXT_LENGTH)
  email = models.EmailField()
  def __unicode__ (self):
    return str(self.item_lost)

class FoundItems(models.Model):
  user = models.ForeignKey(User)
  item_found = models.CharField(max_length = MC.TEXT_LENGTH)
  category = models.CharField(max_length = MC.TEXT_LENGTH, choices=CATEGORY)
  place = models.CharField(max_length = MC.TEXT_LENGTH)
  status = models.CharField(max_length = MC.TEXT_LENGTH)
  other_details = models.TextField(blank=True)
  contact = models.CharField(max_length = 20)
  address = models.CharField(max_length = MC.TEXT_LENGTH)
  email = models.EmailField()
  def __unicode__ (self):
    return str(self.item_found)
