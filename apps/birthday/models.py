from django.db import models
from django.forms import ModelForm
from nucleus.models import User

class BirthdayMessage(models.Model):
  sender = models.ForeignKey(User,related_name='send_birthday_messages')
  receiver = models.ForeignKey(User,related_name='got_birthday_messages')
  message = models.CharField(max_length=500)
  reply = models.CharField(max_length=500,blank = True)
  date = models.DateField(auto_now_add = True)
