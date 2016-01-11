from django.forms import ModelForm
from django import forms
from buyandsell.models import *

class SellForm(ModelForm):
  item_image = forms.ImageField(required=False, error_messages = {'invalid':("Image files only")},widget=forms.FileInput)
  class Meta:
    model =SaleItems
    fields=['item_name','cost','detail','contact','days_till_expiry','email','category','item_image']

class RequestForm(ModelForm):
  class Meta:
    model =RequestedItems
    fields=['item_name','price_upper','contact','days_till_expiry','email','category']

class TransactionForm(ModelForm):
  class Meta:
    model=SuccessfulTransaction


