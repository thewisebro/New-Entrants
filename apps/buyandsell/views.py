from django.shortcuts import render_to_response,render
from core.forms import ModelForm
from django.http import HttpResponseRedirect, HttpResponse
from django.core.mail import send_mail
from django.contrib import messages
from datetime import date, timedelta, datetime
import simplejson
from django.template.response import TemplateResponse
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
    if pu>=0 and pl >=0 and pu>pl:
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
    if pu>=0 and pl >=0 and pu>pl:
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
        return TemplateResponse(request, 'buyandsell/form.html', {'redirect_url':'/buyandsell/buy/'})
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
        return TemplateResponse(request, 'buyandsell/form.html', {'redirect_url':'/buyandsell/viewrequests/'})
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

def selldetails(request,pk):
  item=SaleItems.objects.get(pk=pk)
  self_flag=0
  user=request.user
  username=request.user.username
  item_user=item.user.username
  if username == item_user:
    self_flag=1
  if request.method=='POST':
    password=request.POST.get('password')
    if user.check_password(password):
      sendmail(request,'buy',pk)
    elif password=='':
      messages.error(request, 'Password cant be empty' )
    
    elif not user.check_password(password):
      messages.error(request, 'Incorrect password' )
  context={
    'item':item,
    'self_flag':self_flag
          }
  return render(request,'buyandsell/selldetails.html',context)

def requestdetails(request,pk):
  item=RequestedItems.objects.get(pk=pk)
  self_flag=0
  user=request.user
  username=request.user.username
  item_user=item.user.username
  if username == item_user:
    self_flag=1
  if request.method=='POST':
    password=request.POST.get('password')
    if user.check_password(password):
      sendmail(request,'request',pk)
    elif password=='':
      messages.error(request, 'Password cant be empty' )

    elif not user.check_password(password):
      messages.error(request, 'Incorrect password' )

  context={
    'item':item,
    'self_flag':self_flag
          }
  return render(request,'buyandsell/requestdetails.html',context)

def sendmail(request, type_of_mail, id_pk):
  user = request.user
  username = request.user.username
  sex=request.user.gender
  already_sent=0
  pronoun = "him"
  if sex=="F":
    pronoun="her"
  contact = request.user.contact_no
  app='buyandsell'
  if type_of_mail == 'buy':
    buy_mail_list=BuyMails.objects.filter(by_user__username=username,item__pk=id_pk)
    qryst = SaleItems.objects.filter(pk = id_pk)
    if buy_mail_list:
      messages.error(request,"A mail has already been sent to "+qryst[0].user.first_name+" by you for this item. He may contact you shortly. If not, go ahead and contact "+pronoun+" yourself!")
      already_sent=1
    new_mail_sent=BuyMails(by_user=user,item=qryst[0])
    new_mail_sent.save()
    subject = 'Your item ' + qryst[0].item_name + ' has a buyer on Buy and Sell!'
    msg = 'Your item ' + qryst[0].item_name + ' added by you on ' + str(qryst[0].post_date) + ' has a prospective buyer! '
    msg += user.first_name + ' wants to buy your item. You can contact '+pronoun+' at this number ' + contact
    msg += ' or email '+pronoun+' at ' + str(user.email) + '\nNote: if there is no phone number or email id, that means that ' + user.first_name
    msg += ' has not filled in his contact information in the channel-i database.'
    notif_text = user.first_name + ' wants to buy ' + qryst[0].item_name + ' added by you. '
    if contact:
      notif_text += 'Contact '+pronoun+' at ' + str(contact) + '. '
    if qryst[0].email:
      notif_text += 'Email at ' + str(user.email) + '.'
    url = '/buyandsell/sell_details/' + str(id_pk)
    users = [qryst[0].user]
    Notification.save_notification(app, notif_text, url, users, qryst[0])


  if type_of_mail == 'request':
    qryst = RequestedItems.objects.filter(pk = id_pk)
    buy_mail_list=RequestMails.objects.filter(by_user__username=username,item__pk=id_pk)
    if buy_mail_list:
      messages.error(request,"A mail has already been sent to "+qryst[0].user.first_name+" by you for this item. He may contact you shortly. If not, go ahead and contact "+pronoun+" yourself!")
      already_sent=1
    new_mail_sent=RequestMails(by_user=user,item=qryst[0])
    new_mail_sent.save()
    subject = 'Your request for ' + qryst[0].item_name + ' has been answered!'
    msg = 'Your request ' + qryst[0].item_name + ' added by you on ' + str(qryst[0].post_date) + ' has a prospective seller! \n'
    msg += user.first_name + ' has the item that you requested for. You can contact '+pronoun+' at this number ' + contact
    msg += ' or email '+pronoun+' at ' + str(user.email) + '\n\n Note: if there is no phone number or email id, that means that ' + user.first_name
    msg += ' has not filled in his contact information in the channel-i database.'
    notif_text = user.first_name + ' has an item(' + qryst[0].item_name + ') you requested for. '
    if contact:
      notif_text += 'Contact '+pronoun+' at ' + str(contact) + '. '
    if qryst[0].email:
      notif_text += 'Email at ' + str(user.email) + '.'
    url = '/buyandsell/request_details/' + str(id_pk)
    users = [qryst[0].user]
    Notification.save_notification(app, notif_text, url, users, qryst[0])


  if not already_sent:
    receiver = [str(qryst[0].email),]
    try:
      from django.core.mail import send_mail
      send_mail(subject, msg, 'buysell@iitr.ernet.in', receiver, fail_silently = True)
      email_sent_msg = qryst[0].user.first_name + ' has been sent a mail with your contact information. He may contact you shortly. If not, go ahead and contact '+pronoun+' youself!'
      messages.success(request, email_sent_msg)
    except Exception as e:
      messages.error(request, 'Email has not been sent to ' + qryst[0].user.first_name + '. Error occured and reported.' )
      
def sellformsearch(request):
  srch_string=request.GET.get('keyword')
  query_set=RequestedItems.objects.filter(item_name__icontains=srch_string)
  object_list=[]
  for item in query_set:
    item_dict={}
    item_dict.update({'id':item.pk,'name':item.item_name,'price_upper':item.price_upper})
    object_list.append(item_dict)
  items = simplejson.dumps(object_list)
  return HttpResponse(items, content_type="application/json")

def requestformsearch(request):
  srch_string=request.GET.get('keyword')
  query_set=SaleItems.objects.filter(item_name__icontains=srch_string)
  object_list=[]
  for item in query_set:
    item_dict={}
    item_dict.update({'id':item.pk,'name':item.item_name,'cost':item.cost})
    object_list.append(item_dict)
  items = simplejson.dumps(object_list)
  return HttpResponse(items, content_type="application/json")

