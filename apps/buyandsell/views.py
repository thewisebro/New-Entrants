from django.shortcuts import render_to_response,render
from core.forms import ModelForm
from django.http import HttpResponseRedirect, HttpResponse
from django.core.mail import send_mail
from django.contrib import messages
from datetime import date, timedelta, datetime
import simplejson

from buyandsell.models import *
from buyandsell.constants import *
from notifications.models import Notification
from buyandsell.forms import *

def buy(request,mc=None,c=None):
  qdata=''
  table_data=''
  price_valid=0
  maincategory=''
  category=''
  error_msg=''

  if request.GET.get('ll') and request.GET.get('ul'):
    pl=int(request.GET.get('ll'))
    pu=int(request.GET.get('ul'))
    if pu>0 and pl >0 and pu>pl:
      price_valid=1
    else:
      error_msg= "invalid price range"
      return render(request,'buyandsell/buy.html',{'error_msg':error_msg,'table_data':table_data})
 
  if mc and c:
    cat=BuySellCategory.objects.get(code=c)
    category=cat.name
    maincategory=cat.main_category

  if mc and not c:
    mcatlist=BuySellCategory.objects.filter(main_category=mc)
    maincategory=mcatlist[0].main_category  
   
  if mc and c and price_valid:
    qdata=SaleItems.objects.filter(category__main_category=mc,category__code=c,cost__gte=pl,cost__lte=pu,is_active=True).order_by('-pk')

  elif mc and c and not price_valid: 
    qdata=SaleItems.objects.filter(category__main_category=mc,category__code=c,is_active=True).order_by('-pk')
 
  elif mc and not c  and  price_valid:
    qdata=SaleItems.objects.filter(category__main_category=mc,cost__gte=pl,cost__lte=pu,is_active=True).order_by('-pk')

  elif mc and not c and not price_valid: 
    qdata=SaleItems.objects.filter(category__main_category=mc,is_active=True).order_by('-pk')

  elif  price_valid:
    qdata=SaleItems.objects.filter(cost__gte=pl,cost__lte=pu,is_active=True).order_by('-pk')

  else:
    qdata=SaleItems.objects.filter(is_active=True).order_by('-pk')

  if qdata:
    table_data=qdata
  else:
    error_msg='No items in database'

  context={
    'error_msg':error_msg,
    'table_data':table_data,
    'mc':mc,
    'c':c
          }    
  return render(request,'buyandsell/buy.html',context)


def viewrequests(request,mc=None,c=None):
  qdata=''
  table_data=''
  price_valid=0
  maincategory=''
  category=''
  error_msg=''

  if request.GET.get('ll') and request.GET.get('ul'):

    pl=int(request.GET.get('ll'))
    pu=int(request.GET.get('ul'))
    if pu>0 and pl >0 and pu>pl:
      price_valid=1
    else:
      error_msg= "invalid price range"
      return render(request,'buyandsell/buy.html',{'error_msg':error_msg,'table_data':table_data})

 
  if mc and c:
    cat=BuySellCategory.objects.get(code=c)
    category=cat.name
    maincategory=cat.main_category

  if mc and not c:
    mcatlist=BuySellCategory.objects.filter(main_category=mc)
    maincategory=mcatlist[0].main_category  
   
  if mc and c and price_valid:
    qdata=RequestedItems.objects.filter(category__main_category=mc,category__code=c,price_upper__gte=pl,price_upper__lte=pu,is_active=True).order_by('-pk')

  elif mc and c and not price_valid: 
    qdata=RequestedItems.objects.filter(category__main_category=mc,category__code=c,is_active=True).order_by('-pk')
 
  elif mc and not c  and  price_valid:
    qdata=RequestedItems.objects.filter(category__main_category=mc,price_upper__gte=pl,price_upper__lte=pu,is_active=True).order_by('-pk')

  elif mc and not c and not price_valid: 
    qdata=RequestedItems.objects.filter(category__main_category=mc,is_active=True).order_by('-pk')

  elif  price_valid:
    qdata=RequestedItems.objects.filter(price_upper__gte=pl,price_upper__lte=pu,is_active=True).order_by('-pk')

  else:
    qdata=RequestedItems.objects.filter(is_active=True).order_by('-pk')

  if qdata:
    table_data=qdata
  else:
    error_msg='No items in database'

  context={
    'error_msg':error_msg,
    'table_data':table_data,
    'mc':mc,
    'c':c
          }    
  return render(request,'buyandsell/show_requests.html',context)

def sell(request):
  post_date=date.today()
  user=request.user
  contact=request.user.contact_no
  if request.method=='POST':
    form=SellForm(request.POST,request.FILES)
    digcheck=0
    negcheck=0
    lencheck=0
    zercheck=0
    if form.is_valid():
      phone=form.cleaned_data['contact']
      cost=form.cleaned_data['cost']
      if phone.isdigit():
        digcheck=1

      if  len(phone)==len(str(int(phone))):
        zercheck=1

      if len(phone) == 10:
        lencheck=1

      if cost>=0:
        negcheck=1
      if digcheck and negcheck and zercheck and lencheck and zercheck:
        new_item=form.save(commit=False)
        expiry_date=post_date+timedelta(days=form.cleaned_data['days_till_expiry'])
        new_item.post_date=post_date
        new_item.expiry_date=expiry_date
        new_item.user=user
        new_item.save()
      else:
        print "form filled wrongly"
    else:
      return render(request,'buyandsell/form.html',{'form':form})
  init_dict={
             'email':request.user.email,
             'contact':contact,
            }
  form=SellForm(initial=init_dict)
  return render(request,'buyandsell/form.html',{'form':form})

def requestitem(request):
  post_date=date.today()
  user=request.user
  contact=request.user.contact_no
  if request.method=='POST':
    form=RequestForm(request.POST,request.FILES)
    digcheck=0
    negcheck=0
    lencheck=0
    zercheck=0
    if form.is_valid():
      phone=form.cleaned_data['contact']
      price_upper=form.cleaned_data['price_upper']
      if phone.isdigit():
        digcheck=1

      if  len(phone)==len(str(int(phone))):
        zercheck=1

      if len(phone) == 10:
        lencheck=1

      if price_upper>=0:
        negcheck=1
      if digcheck and negcheck and zercheck and lencheck and zercheck:
        new_item=form.save(commit=False)
        expiry_date=post_date+timedelta(days=form.cleaned_data['days_till_expiry'])
        new_item.post_date=post_date
        new_item.expiry_date=expiry_date
        new_item.user=user
        new_item.save()
      else:
        print "form filled wrongly"
    else:
      return render(request,'buyandsell/form.html',{'form':form})
  init_dict={
             'email':request.user.email,
             'contact':contact,
            }
  form=RequestForm(initial=init_dict)
  return render(request,'buyandsell/form.html',{'form':form})
     
def watch(request,mc=None,c=None):

  user=request.user
  if mc and not c:
    cat_list=BuySellCategory.objects.filter(main_category=mc)
    for cat in cat_list:
      cat.watch_users.add(user)
      cat.save()

  if mc and c:
    catg=BuySellCategory.objects.get(code=c)
    catg.watch_users.add(user)
    catg.save()

  success = {'success' : 'true'}
  success = simplejson.dumps(success)
  return HttpResponse(success, content_type="application/json")

