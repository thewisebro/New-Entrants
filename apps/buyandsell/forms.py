from django.forms import ModelForm
from buyandsell.models import *

class SellForm(ModelForm):
  class Meta:
    model =SaleItems
    fields=['item_name','cost','status','detail','contact','days_till_expiry','email','category','item_image']

class RequestForm(ModelForm):
  class Meta:
    model =RequestedItems
    fields=['item_name','price_upper','condition','contact','days_till_expiry','email','category']

class TransactionForm(ModelForm):
  class Meta:
    model=SuccessfulTransaction
    

   


