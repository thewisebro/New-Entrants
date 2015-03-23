from django.shortcuts import render_to_response,render
from core.forms import ModelForm
from django.http import HttpResponseRedirect, HttpResponse
from django.core.mail import send_mail
from django.contrib import messages
from datetime import date, timedelta, datetime
from django.utils import timezone
import simplejson
from django.template.response import TemplateResponse
from buyandsell.models import *
from buyandsell.constants import *
from notifications.models import Notification
from buyandsell.forms import *
from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def buy(request,mc=None,c=None):
  
  qdata=''
  table_data=''
  price_valid=0
  maincategory=''
  category=''
  error_msg=''

  cat_dict=get_category_dictionary()
  if request.GET.get('ll') and request.GET.get('ul'):
    pl=int(request.GET.get('ll'))
    pu=int(request.GET.get('ul'))
    if pu>=0 and pl >=0 and pu>pl:
      price_valid=1
    else:
      error_msg= "invalid price range"
      return render(request,'buyandsell/buy.html',{'error_msg':error_msg,'table_data':table_data,'cat_dict':cat_dict})

  if mc and c:
    cat=BuySellCategory.objects.get(code=c)
    category=cat.name
    maincategory=cat.main_category

  if mc and not c:
    mcatlist=BuySellCategory.objects.filter(main_category=mc)
    maincategory=mcatlist[0].main_category
  if mc and c and price_valid:
    qdata=SaleItems.items.filter(category__main_category=mc,category__code=c,cost__gte=pl,cost__lte=pu,is_active=True).order_by('-pk')
  elif mc and c and not price_valid:
    qdata=SaleItems.items.filter(category__main_category=mc,category__code=c,is_active=True).order_by('-pk')
  elif mc and not c  and  price_valid:
    qdata=SaleItems.items.filter(category__main_category=mc,cost__gte=pl,cost__lte=pu,is_active=True).order_by('-pk')
  elif mc and not c and not price_valid:
    qdata=SaleItems.items.filter(category__main_category=mc,is_active=True).order_by('-pk')
  elif  price_valid:
    qdata=SaleItems.items.filter(cost__gte=pl,cost__lte=pu,is_active=True).order_by('-pk')
  else:
    qdata=SaleItems.items.filter(is_active=True).order_by('-pk')
  if qdata:
    table_data=qdata
  else:
    error_msg='No items in database'

  paginator = Paginator(table_data, 10)
  page = request.GET.get('page', 1)
  page_list = _get_page_list(page, paginator.num_pages, 10)
  try:
    table_data = paginator.page(page)
  except PageNotAnInteger:
    logger.info(request.user.username+": pagination error PageNotAnInteger")
    table_data = paginator.page(1)
  except EmptyPage:
    logger.info(request.user.username+": pagination error EmptyPage")
    table_data = paginator.page(paginator.num_pages)

  context={
    'error_msg':error_msg,
    'table_data':table_data,
    'mc':mc,
    'c':c,
    'cat_dict':cat_dict,
    'paginator':paginator,
    'page_list':page_list
          }
  return render(request,'buyandsell/buy.html',context)


def viewrequests(request,mc=None,c=None):
  qdata=''
  table_data=''
  price_valid=0
  maincategory=''
  category=''
  error_msg=''
  cat_dict=get_category_dictionary()

  if request.GET.get('ll') and request.GET.get('ul'):
    pl=int(request.GET.get('ll'))
    pu=int(request.GET.get('ul'))
    if pu>=0 and pl >=0 and pu>pl:
      price_valid=1
    else:
      error_msg= "invalid price range"
      return render(request,'buyandsell/buy.html',{'error_msg':error_msg,'table_data':table_data,'cat_dict':cat_dict})
  if mc and c:
    cat=BuySellCategory.objects.get(code=c)
    category=cat.name
    maincategory=cat.main_category
  if mc and not c:
    mcatlist=BuySellCategory.objects.filter(main_category=mc)
    maincategory=mcatlist[0].main_category
  if mc and c and price_valid:
    qdata=RequestedItems.items.filter(category__main_category=mc,category__code=c,price_upper__gte=pl,price_upper__lte=pu,is_active=True).order_by('-pk')
  elif mc and c and not price_valid:
    qdata=RequestedItems.items.filter(category__main_category=mc,category__code=c,is_active=True).order_by('-pk')
  elif mc and not c  and  price_valid:
    qdata=RequestedItems.items.filter(category__main_category=mc,price_upper__gte=pl,price_upper__lte=pu,is_active=True).order_by('-pk')
  elif mc and not c and not price_valid:
    qdata=RequestedItems.items.filter(category__main_category=mc,is_active=True).order_by('-pk')
  elif  price_valid:
    qdata=RequestedItems.items.filter(price_upper__gte=pl,price_upper__lte=pu,is_active=True).order_by('-pk')
  else:
    qdata=RequestedItems.items.filter(is_active=True).order_by('-pk')
  if qdata:
    table_data=qdata
  else:
    error_msg='No items in database'

  paginator = Paginator(table_data, 10)
  page = request.GET.get('page', 1)
  page_list = _get_page_list(page, paginator.num_pages, 10)
  try:
    table_data = paginator.page(page)
  except PageNotAnInteger:
    logger.info(request.user.username+": pagination error PageNotAnInteger")
    table_data = paginator.page(1)
  except EmptyPage:
    logger.info(request.user.username+": pagination error EmptyPage")
    table_data = paginator.page(paginator.num_pages)


  context={
    'error_msg':error_msg,
    'table_data':table_data,
    'mc':mc,
    'c':c,
    'cat_dict':cat_dict,
    'paginator':paginator,
    'page_list':page_list
          }
  return render(request,'buyandsell/show_requests.html',context)

def sell(request):
  post_date=timezone.now()
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
      if digcheck and negcheck and zercheck and lencheck:
        new_item=form.save(commit=False)
        expiry_date=post_date+timedelta(days=form.cleaned_data['days_till_expiry'])
        new_item.post_date=post_date
        new_item.expiry_date=expiry_date
        new_item.user=user
        new_item.save()
        app='buyandsell'
        watch_user_list=new_item.category.watch_users.all()
        print watch_user_list
        notif_text=str(new_item.item_name)+"has been added to the category"+str(new_item.category.name)
        notif_text+="that you have watched"
        url = '/buyandsell/sell_details/' + str(new_item.pk)
        Notification.save_notification(app, notif_text, url, watch_user_list, new_item)
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
  post_date=timezone.now()
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
      if digcheck and negcheck and zercheck and lencheck:
        new_item=form.save(commit=False)
        expiry_date=post_date+timedelta(days=form.cleaned_data['days_till_expiry'])
        new_item.post_date=post_date
        new_item.expiry_date=expiry_date
        new_item.user=user
        new_item.save()
        app='buyandsell'
        watch_user_list=new_item.category.watch_users.all()
        print watch_user_list
        notif_text=str(new_item.item_name)+"has been requested in the category"+str(new_item.category.name)
        notif_text+="that you have watched"
        url = '/buyandsell/sell_details/' + str(new_item.pk)
        Notification.save_notification(app, notif_text, url, watch_user_list, new_item)
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

    if not already_sent:
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
      url = '/buyandsell/sell_details/' + str(id_pk)   #this page is to be made
      users = [qryst[0].user]
      Notification.save_notification(app, notif_text, url, users, qryst[0])


  if type_of_mail == 'request':
    qryst = RequestedItems.objects.filter(pk = id_pk)
    buy_mail_list=RequestMails.objects.filter(by_user__username=username,item__pk=id_pk)
    if buy_mail_list:
      messages.error(request,"A mail has already been sent to "+qryst[0].user.first_name+" by you for this item. He may contact you shortly. If not, go ahead and contact "+pronoun+" yourself!")
      already_sent=1

    if not already_sent:
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
      send_mail(subject, msg, 'buysell@iitr.ernet.in', receiver, fail_silently = True)
      email_sent_msg = qryst[0].user.first_name + ' has been sent a mail with your contact information. He may contact you shortly. If not, go ahead and contact '+pronoun+' youself!'
      messages.success(request, email_sent_msg)
    except Exception as e:
      messages.error(request, 'Email has not been sent to ' + qryst[0].user.first_name + '. Error occured and reported.' )

def search(request,search_type):
  main_dict={}
  srch_string=request.GET.get('keyword','')
  words=srch_string.split(' ')

  if search_type=="sell" or search_type=="main" :
    queryset=[]
    un_queryset = {}
    count = {}
    print words
    for word in words:
      result = RequestedItems.items.filter(item_name__icontains=word,is_active=True)
      for temp in result:
        print word
        if temp.id in un_queryset:
          count[temp.id] = count[temp.id]+1
        else:
          un_queryset[temp.id] = temp
          count[temp.id] = 1
    date_sorted_queryset=sorted(un_queryset, key= lambda l : un_queryset[l].expiry_date, reverse=True)
    count_date_sorted_queryset=sorted(date_sorted_queryset, key= lambda l: count[l], reverse=True)
    for item_id in count_date_sorted_queryset:
      queryset.append(un_queryset[item_id])
    object_list=[]
    for item in queryset:
      item_dict={}
      item_dict.update({'id':item.pk,'name':item.item_name,'price_upper':item.price_upper})
      object_list.append(item_dict)
    items = simplejson.dumps(object_list)
    if search_type=="main":
      main_dict['requests']=object_list[0:5]

  if search_type=="request" or search_type=="main":
    queryset=[]
    un_queryset = {}
    count = {}
    print words
    for word in words:
      result = SaleItems.items.filter(item_name__icontains=word,is_active=True)
      for temp in result:
        print word
        if temp.id in un_queryset:
          count[temp.id] = count[temp.id]+1
        else:
          un_queryset[temp.id] = temp
          count[temp.id] = 1
    date_sorted_queryset=sorted(un_queryset, key= lambda l : un_queryset[l].expiry_date, reverse=True)
    count_date_sorted_queryset=sorted(date_sorted_queryset, key= lambda l: count[l], reverse=True)
    for item_id in count_date_sorted_queryset:
      queryset.append(un_queryset[item_id])
    object_list=[]
    for item in queryset:
      item_dict={}
      item_dict.update({'id':item.pk,'name':item.item_name,'cost':item.cost})
      object_list.append(item_dict)
    items = simplejson.dumps(object_list)
    if search_type=="main":
      main_dict['sell_items']=object_list[0:5]


  if search_type=="main":
#sub-category matched items
    queryset=[]
    un_queryset = {}
    count = {}
    print words
    for word in words:
      result = BuySellCategory.objects.filter(name__icontains=word)
      for temp in result:
        print word
        if temp.id in un_queryset:
          count[temp.id] = count[temp.id]+1
        else:
          un_queryset[temp.id] = temp
          count[temp.id] = 1
    count_sorted_queryset=sorted(un_queryset, key= lambda l: count[l], reverse=True)
    for item_id in count_sorted_queryset:
      queryset.append(un_queryset[item_id])
    object_list=[]
    for item in queryset:
      item_dict={}
      item_dict.update({'id':item.pk,'main_category':item.main_category,'code':item.code,'name':item.name})
      object_list.append(item_dict)
    main_dict['sub_cat']=object_list

# main_category matched items
    queryset=[]
    un_queryset = {}
    count = {}
    print words
    for word in words:
      result = BuySellCategory.objects.filter(main_category__icontains=word)
      for temp in result:
        print word
        if temp.main_category in un_queryset:
          count[temp.main_category] = count[temp.main_category]+1            #done this way because many category objects can have the same main category
        else:
          un_queryset[temp.main_category] = temp
          count[temp.main_category] = 1
    count_sorted_queryset=sorted(un_queryset, key= lambda l: count[l], reverse=True)
    for main_category in count_sorted_queryset:
      queryset.append(un_queryset[main_category])
    object_list=[]
    for item in queryset:
      item_dict={}
      item_dict.update({'id':item.pk,'main_category':item.main_category,'code':item.code,'name':item.name})
      object_list.append(item_dict)
    main_dict['main_cat']=object_list

  print items
  print main_dict
  if search_type=="main":
    return HttpResponse(simplejson.dumps(main_dict), content_type="application/json")
  else:
    return HttpResponse(items, content_type="application/json")


def seeall(request,search_type):
  main_dict={}
  srch_string=request.GET.get('keyword','')
  word_list=srch_string.split(' ')
  words=[]
  for word in word_list:
    if word !='':
      words.append(word)

  if search_type=="requests" :
    queryset=[]
    un_queryset = {}
    count = {}
    print words
    for word in words:
      result = RequestedItems.items.filter(item_name__icontains=word,is_active=True)
      for temp in result:
        print word
        if temp.id in un_queryset:
          count[temp.id] = count[temp.id]+1
        else:
          un_queryset[temp.id] = temp
          count[temp.id] = 1
    date_sorted_queryset=sorted(un_queryset, key= lambda l : un_queryset[l].expiry_date, reverse=True)
    count_date_sorted_queryset=sorted(date_sorted_queryset, key= lambda l: count[l], reverse=True)
    for item_id in count_date_sorted_queryset:
      queryset.append(un_queryset[item_id])
    return render(request,'buyandsell/show_requests.html',{'table_data':queryset})

  if search_type=="sell":
    queryset=[]
    un_queryset = {}
    count = {}
    print words
    for word in words:
      result = SaleItems.items.filter(item_name__icontains=word,is_active=True)
      for temp in result:
        print word
        if temp.id in un_queryset:
          count[temp.id] = count[temp.id]+1
        else:
          un_queryset[temp.id] = temp
          count[temp.id] = 1
    date_sorted_queryset=sorted(un_queryset, key= lambda l : un_queryset[l].expiry_date, reverse=True)
    count_date_sorted_queryset=sorted(date_sorted_queryset, key= lambda l: count[l], reverse=True)
    for item_id in count_date_sorted_queryset:
      queryset.append(un_queryset[item_id])
    return render(request,'buyandsell/buy.html',{'table_data':queryset})

def edit(request,form_type,pk):
  user=request.user
  post_date=date.today()
  if form_type=="sell":
    instance=SaleItems.objects.get(pk=pk)
    old_category=instance.category
    if request.method=='POST':
      form=SellForm(request.POST,request.FILES,instance=instance)
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
          edited_item=form.save(commit=False)
          expiry_date=post_date+timedelta(days=form.cleaned_data['days_till_expiry'])
          edited_item.post_date=post_date
          edited_item.expiry_date=expiry_date
          edited_item.user=user
          edited_item.save()
          if edited_item.category !=  old_category:
            app='buyandsell'
            watch_user_list=edited_item.category.watch_users.all()
            print watch_user_list
            notif_text=str(edited_item.item_name)+"has been added in the category"+str(edited_item.category.name)
            notif_text+="that you have watched"
            url = '/buyandsell/sell_details/' + str(edited_item.pk)
            Notification.save_notification(app, notif_text, url, watch_user_list, edited_item)
          return TemplateResponse(request, 'buyandsell/form.html', {'redirect_url':'/buyandsell/my-account/'})
        else:
          print "form filled wrongly"
      else:
        return render(request,'buyandsell/form.html',{'form':form})
    form=SellForm(instance=instance)
    return render(request,'buyandsell/form.html',{'form':form})

  if form_type=="request":
    instance=RequestedItems.objects.get(pk=pk)    #update notifications to be given to watch users
    old_category=instance.category
    if request.method=='POST':
      form=RequestForm(request.POST,request.FILES,instance=instance)
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
          edited_item=form.save(commit=False)
          expiry_date=post_date+timedelta(days=form.cleaned_data['days_till_expiry'])
          edited_item.post_date=post_date
          edited_item.expiry_date=expiry_date
          edited_item.user=user
          edited_item.save()
          if edited_item.category !=  old_category:
            app='buyandsell'
            watch_user_list=edited_item.category.watch_users.all()
            print watch_user_list
            notif_text=str(edited_item.item_name)+"has been requested in the category"+str(edited_item.category.name)
            notif_text+="that you have watched"
            url = '/buyandsell/sell_details/' + str(edited_item.pk)
            Notification.save_notification(app, notif_text, url, watch_user_list, edited_item)
          return TemplateResponse(request, 'buyandsell/form.html', {'redirect_url':'/buyandsell/my-account/'})
        else:
          print "form filled wrongly"
      else:
        return render(request,'buyandsell/form.html',{'form':form})
    form=RequestForm(instance=instance)
    return render(request,'buyandsell/form.html',{'form':form})

def my_account(request):
  show_contact=1
  user=request.user
  sell_items=SaleItems.items.filter(user=user).order_by('-pk')
  request_items=RequestedItems.items.filter(user=user).order_by('-pk')
  main_watched_cat,sub_watched_cat=get_watched_categories(request)
  
  if len(ShowContact.objects.filter(user=user))==1:
    if ShowContact.objects.filter(user=user)[0].contact_shown==0:
      show_contact=0
  
  context={'sell_items':sell_items,
           'request_items':request_items,
           'main_watched_cat':main_watched_cat,
           'sub_watched_cat':sub_watched_cat,
           'show_contact':show_contact
          }
 
  return render(request,'buyandsell/myaccount.html',context) 

def get_category_dictionary():
  cat_dict={}
  main_cat=[]
  cat_list=BuySellCategory.objects.all()
  for cat in cat_list:
    if cat.main_category not in main_cat:
      main_cat.append(cat.main_category)
  for mcat in main_cat:
    sub_cat=BuySellCategory.objects.filter(main_category=mcat)
    cat_dict[mcat]=sub_cat
  return cat_dict  

def trash_item(request,item_type,pk):
  if item_type=="request":
    item=RequestedItems.items.get(pk=pk)
    item.trash()

  else:
    item=SaleItems.items.get(pk=pk)
    item.trash()

  success = {'success' : 'true'}
  success = simplejson.dumps(success)
  return HttpResponse(success, content_type="application/json")

def transaction(request,item_type,pk):
  user=request.user
  if item_type=="sell":
    if request.method=="POST":
      form=TransactionForm()
      buyer_username=request.POST.get('buyer_username')
      print buyer_username
      if buyer_username != "":
        buyer=User.objects.get(username=buyer_username)
      else:
        buyer=None
      new_item=form.save(commit=False)
      if  not  request.POST.get('feedback').isspace() and  request.POST.get('feedback')!="":
        new_item.feedback=request.POST.get('feedback')
      else:
        messages.error(request,"Feedback cant be empty")
        return HttpResponseRedirect('/buyandsell/succ_trans/sell/'+pk+'/')
      new_item.seller=user
      new_item.buyer=buyer
      sell_item=SaleItems.objects.get(pk=pk)
      new_item.sell_item=sell_item
      new_item.trasaction_date=timezone.now()
      new_item.save()      
    sell_item=SaleItems.objects.get(pk=pk)
    mail_list=BuyMails.objects.filter(item=sell_item)  
    return render(request,'buyandsell/trans_form.html',{'mail_list':mail_list,'type':item_type})

  if item_type=="request":
    if request.method=="POST":
      form=TransactionForm()
      seller_username=request.POST.get('seller_username')
      if seller_username !="":
        seller=User.objects.get(username=seller_username)
      else:
        seller=None
      new_item=form.save(commit=False)
      if  not  request.POST.get('feedback').isspace() and  request.POST.get('feedback')!="":
        new_item.feedback=request.POST.get('feedback')
      else:
        messages.error(request,"Feedback cant be empty")
        return HttpResponseRedirect('/buyandsell/succ_trans/request/'+pk+'/')
      new_item.seller=seller
      new_item.buyer=user
      request_item=RequestedItems.objects.get(pk=pk)
      new_item.request_item=request_item        #need to redirect if already existing request item or sell item is present
      new_item.is_requested=True
      new_item.trasaction_date=timezone.now()
      new_item.save()      
    request_item=RequestedItems.objects.get(pk=pk)
    mail_list=RequestMails.objects.filter(item=request_item)
    return render(request,'buyandsell/trans_form.html',{'mail_list':mail_list})
  
def  get_watched_categories(request):
  user=request.user
  cat_dict=get_category_dictionary()
  main_watched_cat=[]
  sub_watched_cat=[]
  for main_cat,cat_list in cat_dict.iteritems():
    count=0
    cat_len=len(cat_list)
    for cat in cat_list:
      if user in cat.watch_users.all():
        sub_watched_cat.append(cat)
        count=count+1
    if count==cat_len:
      main_watched_cat.append(main_cat)
  print "main"
  print main_watched_cat
  print "sub"
  print sub_watched_cat
  return main_watched_cat,sub_watched_cat

def show_contact(request,response):
  user=request.user
  if response=="yes":
    if len(ShowContact.objects.filter(user=user))==0:
      item=ShowContact(user=user)
      item.save()
    else:
      item=ShowContact.objects.get(user=user)
      item.contact_shown=True
      item.save()

  else:
    if len(ShowContact.objects.filter(user=user))==0:
      item=ShowContact(user=user,contact_shown=False)
      item.save()
    else:
      item=ShowContact.objects.get(user=user)
      item.contact_shown=False
      item.save()

  success = {'success' : 'true'}
  success = simplejson.dumps(success)
  return HttpResponse(success, content_type="application/json")

def manage(request):
  user=request.user
  cat_dict=get_category_dictionary()
  main_watched_cat,sub_watched_cat=get_watched_categories(request)
  old_watched_list=[]

  for cat in sub_watched_cat:
    old_watched_list.append(cat.id)

  if request.method=='POST':
    new_watched_list=request.POST.getlist('watched_category')
    new_watched_list=[int(i) for i in new_watched_list]
    for cat_id in new_watched_list:
      if cat_id not in old_watched_list:
        cat=BuySellCategory.objects.get(pk=cat_id)
        cat.watch_users.add(user)
        cat.save()
    for cat_id in old_watched_list:
      if cat_id not in new_watched_list:
        cat=BuySellCategory.objects.get(pk=cat_id)
        cat.watch_users.remove(user)
        cat.save()
    main_watched_cat,sub_watched_cat=get_watched_categories(request)
    return TemplateResponse(request, 'buyandsell/form.html', {'redirect_url':'/buyandsell/my-account/'})
  return render(request,'buyandsell/manage.html',{'cat_dict':cat_dict,'main_watched_cat':main_watched_cat,'sub_watched_cat':sub_watched_cat})

def _get_page_list(page_no, pages, items_per_page):
  l = range(1, pages+1)
  page_no = int(page_no)

  items_per_page /= 2
  if page_no in l[0:items_per_page]:
    return l[0:2*items_per_page]

  elif page_no in l[-items_per_page:]:
    return l[-2*items_per_page:]

  else:
    return l[page_no - items_per_page + 1: page_no + items_per_page - 1]


