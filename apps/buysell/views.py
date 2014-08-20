from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from core.forms import ModelForm
from django.http import HttpResponse, Http404
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from django.template import RequestContext
from django.core import serializers
from django.contrib import messages
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files.base import ContentFile
from django.core.files import File
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings

from buysell.forms import *
from datetime import date, timedelta, datetime
from buysell.models import *
from buysell.constants import *
from notifications.models import Notification

MEDIA_ROOT = settings.MEDIA_ROOT
MEDIA_URL = settings.MEDIA_URL

import os, logging
import re

from PIL import Image
import StringIO
from urlparse import urlparse
import urllib2
import collections

logger = logging.getLogger('buysell')

@login_required
def buysell(request):
  logger.info(request.user.username+": in homepage.")
  return HttpResponseRedirect('/buysell/buy/')

@login_required
def sell(request):
  logger.info(request.user.username + ': in sell')
  post_date = date.today()
  expiry_date = post_date + timedelta(days=90)
  user=request.user

  p=0
  contact = request.user.contact_no
  if request.method == 'POST':  #form has been submitted
    logger.info(request.user.username + ': submitted form for sell')
    form = BaseModelFormFunction(ItemsForSale , ['user', 'post_date', 'expiry_date'], data=request.POST, files=request.FILES)
    # image_entry = ItemsForSale()
    ver=0
    flag=0
    lencheck=0
    negcheck=0
    splcheck=0
    if form.is_valid():
      phone=form.cleaned_data['contact']
      cost=form.cleaned_data['cost']
      name=form.cleaned_data['item_name']
      if phone.isdigit():
        ver=1

      if not len(phone)==len(str(int(phone))):
        messages.success(request,"Phone number should not start with zero and should contain exactly 10 digits.")
        return HttpResponseRedirect('/buysell/sell/')
      if len(phone) == 10:
        lencheck=1

      if cost>=0:
        negcheck=1
      if special_match(name):
        splcheck=1
    if form.is_valid() and ver and lencheck and negcheck and splcheck:
      if request.FILES:
        image = Image.open(request.FILES['item_image'])
        wt,ht=image.size
        fmt = image.format
        new_wt = 400
        new_ht = (ht * new_wt) // wt
        image = image.resize((new_wt, new_ht), Image.ANTIALIAS)
        image_io = StringIO.StringIO()
        image.convert("RGB")
        try:
          image.save(image_io, format = 'JPEG', quality=90)
          image_file = InMemoryUploadedFile(image_io, None, str(form.cleaned_data['item_name']), 'image/jpeg', image_io.len, None)
        except Exception as e:
          logger.info(request.user.username + ': got en error in saving item image for sale.')
          logger.info(e)
          image.save(image_io, format = fmt)
          image_file = InMemoryUploadedFile(image_io, None, str(form.cleaned_data['item_name']), 'image/'+fmt.lower(), image_io.len, None)
        image_entry = ItemsForSale()
        image_entry.item_image = image_file
      """
      else:
        default_img_url = MEDIA_ROOT + '/buysell/images/default.png'
        f = File(open(default_img_url,'r'))
        name = 'default'
        content = ContentFile(f.read())
        image_entry.item_image.save('default.png', content, save=False)
      """
      expiry_date = post_date + timedelta(days=form.cleaned_data['days_till_expiry'])
      new_entry = form.save(commit=False)
      new_entry.item_name = str(new_entry.item_name).capitalize()
      new_entry.user = request.user
      new_entry.post_date = post_date
      new_entry.expiry_date = expiry_date
      if request.FILES:
        new_entry.item_image = image_entry.item_image
      try:
        new_entry.save()
      except Exception as e:
        messages.error(request, 'Well, this is embarassing. Due to an error, your entry was not saved. The error has been reported')
        logger.info(request.user.username + ': error in saving items for sale.')
        logger.info(e)
        return HttpResponseRedirect('/buysell/')
      else:
        messages.success(request, 'Item added!')
        logger.info(request.user.username + ': saved item with item pk ' + str(new_entry.pk))
        return HttpResponseRedirect('/buysell/buy_item_details/' + str(new_entry.pk))
    elif ver==0 and form.is_valid():
      messages.error(request,'Only numeric value should be entered in Phone No.')
    elif lencheck==0 and form.is_valid():
      messages.error(request,'Phone number should be 10 digits long.')
    elif splcheck==0 and form.is_valid():
      messages.error(request,'Item name should be a alphanumeric value. No special characters are allowed.')
    elif negcheck==0 and form.is_valid():
      messages.error(request,'Price field should given a positive value.')
    else:
      messages.error(request, 'Form filled wrongly')
      print form.errors
      form = BaseModelFormFunction(ItemsForSale , ['user', 'post_date', 'expiry_date' ],data = request.POST, files = request.FILES)
      return render_to_response('buysell/sell1.html', { 'form': form,'contact':contact}, context_instance=RequestContext(request) )

  else:
    email = request.user.email

    initDict = {
       'email':email
       }
    form = BaseModelFormFunction(ItemsForSale , ['user', 'post_date', 'expiry_date' ], initial = initDict)
  return render_to_response('buysell/sell1.html', { 'form': form,'contact':contact}, context_instance=RequestContext(request) )

@login_required
def request_item(request):
  user=request.user
  contact = request.user.contact_no
  flag=0
  ver=0
  lencheck=0
  negcheck=0
  splcheck=0
  if request.method == 'POST':
    logger.info(request.user.username + ': submitted form for sell')
    post_date = date.today()
    expiry_date = post_date + timedelta(days=90)
    form = BaseModelFormFunction(ItemsRequested , [ 'user', 'post_date', 'expiry_date'], request.POST)
    if form.is_valid():
      price_upper=form.cleaned_data['price_upper']
      name=form.cleaned_data['item_name']
      phone=form.cleaned_data['contact']
      if phone.isdigit():
        ver=1
      if not len(phone)==len(str(int(phone))):
        messages.success(request,"Phone number should not start with zero and should contain exactly 10 digits.")
        return HttpResponseRedirect('/buysell/request-item/')

      if len(phone)==10:
        lencheck=1

      if price_upper>0:
        negcheck=1

      if special_match(name):
        splcheck=1
    if form.is_valid() and ver and lencheck and negcheck and splcheck:
      new_entry = form.save(commit=False)
      new_entry.item_name = str(new_entry.item_name).capitalize()
      new_entry.user = request.user
      new_entry.post_date = post_date
      new_entry.expiry_date = expiry_date
      new_entry.price_lower=0
      try :
        new_entry.save()
      except Exception as e :
        logger.info(request.user.username + ': error in saving items requested.')
        logger.info(e)
        messages.error(request, 'Well, this is embarassing. Due to an error, your entry was not saved. Please try later.')
        return HttpResponseRedirect('/buysell/')
      else:
        messages.success(request, 'Request added')
        logger.info(request.user.username + ': saved request with item pk ' + str(new_entry.pk))
        return HttpResponseRedirect('/buysell/requested_item_details/' + str(new_entry.pk))
    elif (ver==0 or lencheck==0 or negcheck==0 or splcheck==0) and form.is_valid():
      if ver==0:
        messages.error(request,'Only numeric value should be entered in Phone No.')
      if lencheck==0:
        messages.error(request,'Phone number should be 10 digits long.')
      if splcheck==0:
        messages.error(request,'Item name should be given a alphanumeric value. No special characters are allowed.')
      if negcheck==0:
        messages.error(request,'Price fields should be given a positive value.')
    else:
      messages.error(request, 'Form filled wrongly')
      form = BaseModelFormFunction(ItemsRequested , ['user', 'post_date', 'expiry_date' ],data = request.POST)
      return render_to_response('buysell/addrequest.html', { 'form': form, 'contact':contact}, context_instance=RequestContext(request) )


  else:
    logger.info(request.user.username + ': request added successfully.')
    email = request.user.email
    initDict = {
       'email':email
       }
    form = BaseModelFormFunction(ItemsRequested , ['user', 'post_date', 'expiry_date'], initial = initDict)
  return render_to_response('buysell/addrequest.html',{'form': form,'contact':contact, 'email':email}, context_instance=RequestContext(request) )

@login_required
def viewrequests(request):
  logger.info(request.user.username+": viewed item requests")
  qryst_req = ItemsRequested.objects.all().order_by('-pk')
  paginator = Paginator(qryst_req, 10)
  page = request.GET.get('page', 1)
  try:
    pageTableData = paginator.page(page)
  except PageNotAnInteger:
    logger.info(request.user.username + ': pagination error on buy - PageNotAnInteger.' )
    pageTableData = paginator.page(1)
  except EmptyPage:
    logger.info(request.user.username + ': pagination error on buy - EmptyPage.' )
    pageTableData = paginator.page(paginator.num_pages)
  pages = range(1,(qryst_req.count()+19)/10)
# If only a single page, do not show paging                                |
  if len(pages) == 1 :
    pages = None
  return render_to_response('buysell/view-requests.html', {'table_data':pageTableData,'pages':pages} ,  context_instance=RequestContext(request))

@login_required
def buy(request, mc=None, sc=None):
  logger.info(request.user.username + ': entered buy.')
  table_data = ''
  qryst=''
  mcn=''
  scn=''
  if mc:
    if mc == 'EL':
      mcn='Electronics'
    elif mc == 'BK':
      mcn='Books'
    elif mc == 'MS':
      mcn='Miscellaneous'
  else:
    mcn='Recent'
  if sc:
    if sc == 'LP':
      scn='Computer Accessories'
    elif sc == 'MO':
      scn='Mobile Accessories'
    elif sc == 'OT':
      scn='Other'
    elif sc == 'ED':
      scn='Education'
    elif sc == 'CS':
      scn='Course Books'
    elif sc == 'FC':
      scn='Fiction'
    elif sc == 'TR':
      scn='Trunks'
    elif sc == 'BC':
      scn='Bicycle'
  else:
    scn=''

  if not mc and not sc:
    qryst= ItemsForSale.objects.all().order_by('-pk')
  if mc and not sc:
    logger.info(request.user.username + ': entered buy with category ' + mc)
    qryst = ItemsForSale.objects.filter(category = mc).order_by('-pk')
  if mc and sc:
    logger.info(request.user.username + ': entered buy with category ' + mc + ' and subcat ' + sc)
    qryst = ItemsForSale.objects.filter(category = mc, sub_category = sc).order_by('-pk')
  if not qryst:
    logger.info(request.user.username + ': no item found in buy for the categoty and/or subcat selected.')
  if qryst:
    logger.info(request.user.username + ': query made for ItemsForSale - non-empty.')
    table_data = qryst
  paginator = Paginator(table_data, 10)
  page = request.GET.get('page', 1)

  try:
    pageTableData = paginator.page(page)
  except PageNotAnInteger:
    logger.info(request.user.username + ': pagination error on buy - PageNotAnInteger.' )
    pageTableData = paginator.page(1)
  except EmptyPage:
    logger.info(request.user.username + ': pagination error on buy - EmptyPage.' )
    pageTableData = paginator.page(paginator.num_pages)
  pages = range(1,(qryst.count()+19)/10)
# If only a single page, do not show paging                                |
  if len(pages) == 1 :
    pages = None
  dictionary = {'table_data': pageTableData,'pages':pages, 'mcn':mcn, 'scn':scn,'sc':sc,'mc':mc}
  return render_to_response('buysell/buy.html', dictionary, context_instance = RequestContext(request) )

@login_required
def search(request):
  query=request.GET['query']
  searchIn='buy'
  try:
    searchIn=request.GET['qtype']
  except:
    searchIn='buy'
  logger.info(request.user.username+': entered search query '+query+' in '+searchIn+ ' category')
  user=request.user
  srchflag=1
  if searchIn == 'buy':
    qryst = ItemsForSale.objects.filter(item_name__icontains = query)
    qt_flag=0
  elif searchIn == 'request':
    qryst = ItemsRequested.objects.filter(item_name__icontains = query)
    qt_flag=1
  number_rows=qryst.count()
  paginator = Paginator(qryst, 10)
  page = request.GET.get('page', 1)
  try:
    pageTableData = paginator.page(page)
  except PageNotAnInteger:
    logger.info(request.user.username + ': pagination error on buy - PageNotAnInteger.' )
    pageTableData = paginator.page(1)
  except EmptyPage:
    logger.info(request.user.username + ': pagination error on buy - EmptyPage.' )
    pageTableData = paginator.page(paginator.num_pages)
  if qryst:
    if number_rows==1:
      messages.success(request,'1 result found!')
    else:
      messages.success(request, ''+str(number_rows)+' results found!')
  if searchIn == 'buy':
    return render_to_response('buysell/buy.html',{'table_data':pageTableData,'searchflag':srchflag},context_instance=RequestContext(request))
  elif searchIn == 'request':
    return render_to_response('buysell/view-requests.html',{'table_data':pageTableData,'searchflag':srchflag},context_instance=RequestContext(request))

@login_required
def sendmail(request, type_of_mail, id_pk):
  logger.info(request.user.username + ': entered sendmail.')
  user = request.user
  username = request.user.username
  sex=request.user.person.gender
  pronoun = "him"
  if sex=="F":
    pronoun="her"
  contact = request.user.contact_no
  app='buysell'
  if type_of_mail == 'buy':
    buy_mail_list=BuyMailsSent.objects.filter(by_user__username=user,item__pk=id_pk)
    qryst = ItemsForSale.objects.filter(pk = id_pk)
    if buy_mail_list:
      messages.error(request,"A mail has already been sent to "+qryst[0].user.first_name+" by you for this item. He may contact you shortly. If not, go ahead and contact "+pronoun+" yourself!")
      return HttpResponseRedirect('/buysell/buy_item_details/'+id_pk+'/')
    new_mail_sent=BuyMailsSent(by_user=user,item=qryst[0])
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
    url = '/buysell/buy_item_details/' + str(id_pk)
    users = [qryst[0].user]
    Notification.save_notification(app, notif_text, url, users, qryst[0])


  if type_of_mail == 'request':
    qryst = ItemsRequested.objects.filter(pk = id_pk)
    buy_mail_list=RequestMailsSent.objects.filter(by_user__username=user,item__pk=id_pk)
    if buy_mail_list:
      messages.error(request,"A mail has already been sent to "+qryst[0].user.first_name+" by you for this item. He may contact you shortly. If not, go ahead and contact "+pronoun+" yourself!")
      return HttpResponseRedirect('/buysell/requested_item_details/'+id_pk+'/')
    new_mail_sent=RequestMailsSent(by_user=user,item=qryst[0])
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
    url = '/buysell/requested_item_details/' + str(id_pk)
    users = [qryst[0].user]
    Notification.save_notification(app, notif_text, url, users, qryst[0])

  receiver = [str(qryst[0].email),]
  try:
    from django.core.mail import send_mail
    send_mail(subject, msg, 'buysell@iitr.ernet.in', receiver, fail_silently = False)
    logger.info(request.user.username + ': sendmail successful to' + qryst[0].user.first_name + '.')
    email_sent_msg = qryst[0].user.first_name + ' has been sent a mail with your contact information. He may contact you shortly. If not, go ahead and contact '+pronoun+' youself!'
    messages.success(request, email_sent_msg)
  except Exception as e:
    messages.error(request, 'Email has not been sent to ' + qryst[0].user.first_name + '. Error occured and reported.' )
    logger.info(request.user.username + ': error sendmail to ' + qryst[0].user.first_name)
    logger.info(e)
  if type_of_mail == 'buy':
    return HttpResponseRedirect('/buysell/buy_item_details/'+id_pk+'/')
  if type_of_mail == 'request':
    return HttpResponseRedirect('/buysell/requested_item_details/'+id_pk+'/')

@login_required
def my_account(request):
  logger.info(request.user.username + ': entered my_account.')
  user = request.user.username
  qryst_requested = ItemsRequested.objects.filter(user__username = user).order_by('-pk')
  qryst_added = ItemsForSale.objects.filter(user__username = user).order_by('-pk')
  dictionary = {'items_added':qryst_added, 'requests':qryst_requested}
  return render_to_response('buysell/my-account.html', dictionary, context_instance=RequestContext(request) )


def ajax_request(request, category):
  html = ''
  if request.is_ajax():
    for k, v in SUB_CATEGORY.iteritems():
      if k == category:
        sub_cat = v
        break
    for t in sub_cat:
      html +='<option value="' + t[0] + '">' + t[1] + '</option>'
  return HttpResponse(html)

@login_required
def edit(request, category, itemReqId):
  logger.info(request.user.username + ': entered edit.')
  if(category == 'item'):
    logger.info(request.user.username + ': entered edit with category item.')
    user = request.user.username
    try:
      formData = ItemsForSale.objects.get(pk = itemReqId, user__username = user)
    except:
      logger.info(request.user.username + ': edit - "item" not found with pk '+ pk + '.')
      messages.error(request, 'Item not Found. Item has either been deleted or the item was added by someone else.')
      HttpResponseRedirect('/buysell/my-account/')
    dict_formData=formData.__dict__
    extraData = {
      'item':formData,
      'editFlag':'1',
      'item_image' : formData.item_image,
      'itemid': itemReqId
      }
    form = BaseModelFormFunction(ItemsForSale, ['user', 'post_date', 'expiry_date'], data = dict_formData)
    return render_to_response('buysell/sell.html', { 'form': form,'extraData':extraData,'itemid':itemReqId }, context_instance=RequestContext(request) )
  elif(category == 'request'):
    logger.info(request.user.username + ': entered edit with category request.')
    user = request.user.username
    try:
      formData = ItemsRequested.objects.get(pk = itemReqId, user__username = user)
    except:
      logger.info(request.user.username + ': edit - "request" not found with pk '+ pk + '.')
      messages.error(request, 'Item not Found. Item has either been deleted or the item was palced by someone else')
      HttpResponseRedirect('/buysell/my-account/')

    extraData = {
      'item':formData,
      'editFlag':'1',
      'reqid': itemReqId
      }
    form = BaseModelFormFunction(ItemsRequested, ['user','post_date', 'expiry_date'], instance = formData)
    return render_to_response('buysell/request-item.html', { 'form': form,'extraData':extraData,'itemid':itemReqId }, context_instance=RequestContext(request) )

@login_required
def editsave(request, category, itemReqId):
  logger.info(request.user.username + ': entered editsave in category ' + category + '.' )
  if(category == 'item'):
    post_date = date.today()
    if not 'item_image' in  request.FILES:
      request.FILES['item_image'] = ''

    if request.method == 'POST':  #form has been submitted
      logger.info(request.user.username + ': form submit for editsave.')
      form = BaseModelFormFunction(ItemsForSale , ['user', 'post_date', 'expiry_date'], data=request.POST, files=request.FILES)
      if form.is_valid():
        if(request.FILES['item_image'] != ''):
          image = Image.open(request.FILES['item_image'])
          image = image.resize((400, 300), Image.ANTIALIAS)
          image_io = StringIO.StringIO()
          image.save(image_io, format = 'JPEG', quality=90)
          image_file = InMemoryUploadedFile(image_io, None, str(form.cleaned_data['item_name']), 'image/jpeg', image_io.len, None)
        else:
          image_file = ''
        #For update, we will open the actual item and change its properties
        oldItem = ItemsForSale.objects.get(pk = itemReqId)
        expiry_date = post_date + timedelta(days=form.cleaned_data['days_till_expiry'])
        newEditedForm = form.save(commit=False)
        newEditedForm.post_date = oldItem.post_date
        newEditedForm.datetime_created = datetime.now()
        newEditedForm.item_name = str(newEditedForm.item_name).capitalize()
        newEditedForm.user = request.user
        newEditedForm.expiry_date = expiry_date
        newEditedForm.pk = oldItem.pk
        if image_file != '':
          #oldItem.item_image = image_file
          newEditedForm.item_image = image_file
        else:
          newEditedForm.item_image = oldItem.item_image
        try :
          newEditedForm.save(force_update=True)
        except Exception as e:
          messages.error(request, 'Well, this is embarassing. Due to an error, your entry was not saved. The error has been reported.')
          logger.info(request.user.username + ': error in saving items for sale.')
          logger.info(e)
          return HttpResponseRedirect('/buysell/')
        else:
          messages.success(request, 'Edit Successful')
          return HttpResponseRedirect('/buysell/')
      else:
        messages.error(request, 'Form filled wrongly')
        form = BaseModelFormFunction(ItemsForSale , ['user', 'post_date', 'expiry_date' ],data = request.POST, files = request.FILES)
        return HttpResponseRedirect('/buysell/edit/item/'+str(itemReqId))


    else:
      return HttpResponseRedirect('/buysell/edit/item/'+ str(itemReqId) + '/')

  elif category == "request":
    post_date = date.today()
    if request.method == 'POST':  #form has been submitted
      logger.info(request.user.username + ': form submited in editsave for request.' )
      form = BaseModelFormFunction(ItemsRequested , ['user', 'post_date', 'expiry_date'], data=request.POST)
      if form.is_valid():
        upper_price=form.cleaned_data['price_upper']
        itemReqId = int(itemReqId)
        oldItem = ItemsRequested.objects.get(pk = itemReqId)
        expiry_date = post_date + timedelta(days=30)
        newEditedForm = form.save(commit=False)
        newEditedForm.item_name = str(newEditedForm.item_name).capitalize()
        newEditedForm.post_date = oldItem.post_date
        newEditedForm.user = request.user
        newEditedForm.expiry_date = expiry_date

        newEditedForm.pk = oldItem.pk
        try :
          newEditedForm.save(force_update=True)
        except Exception as e:
          messages.error(request, 'Well, this is embarassing. Due to an error, your entry was not saved. The error has been reported')
          logger.info(request.user.username + ': error in saving items for sale.')
          logger.info(e)
          return HttpResponseRedirect('/buysell/')
        else:
          messages.success(request, 'Edit successful')
          return HttpResponseRedirect('/buysell/requested_item_details/'+ str(itemReqId) + '/')
      else:
        messages.error(request, 'Form filled wrongly')
        form = BaseModelFormFunction(ItemsRequested , ['user', 'post_date', 'expiry_date' ],data = request.POST)
        return HttpResponseRedirect('/buysell/edit/request/'+str(itemReqId)+'/')


    else:
      return HttpResponseRedirect('/buysell/edit/request/'+ itemReqId + '/')

@login_required
def deleteEntry(request, category, pk_id):
  logger.info(request.user.username + ': entered deleteEntry with category ' + category + '.')
  if category == "item":
    item = ItemsForSale.objects.get(pk = pk_id)
    imgPath = MEDIA_ROOT + str(item.item_image)
    if request.user.username == item.user.username:
      try:
        Notification.delete_notification('buysell', item)
        item.delete()
      except:
        messages.error(request, 'An error occured. The error has been reported.')
        logger.info(request.user.username + ': error in deleting items for sale with pk ' + pk_id+ '.')
        logger.info(e)
        return HttpResponseRedirect('/buysell/my-account/')
      else:
        os.remove(imgPath)
        messages.success(request, 'Item successfully deleted.')
        logger.info(request.user.username + ': item deleted with pk ' + pk_id + '.')
        return HttpResponseRedirect('/buysell/my-account/')
    else:
      messages.error(request, 'The item was not posted by you.')
      return HttpResponseRedirect('/buysell/my-account/')

  elif category == "request":
    req = ItemsRequested.objects.get(pk = pk_id)
    if request.user.username == req.user.username:
      try:
        Notification.delete_notification('buysell', req)
        req.delete()
      except Exception as e:
        messages.error(request, 'An error occured. The error has been reported.')
        logger.info(request.user.username + ': error in deleting items requested with pk ' + pk_id+ '.')
        logger.info(e)
        return HttpResponseRedirect('/buysell/my-account/')
      else:
        messages.success(request, 'Request successfully deleted.')
        logger.info(request.user.username + ': item deleted with pk ' + pk_id + '.')
        return HttpResponseRedirect('/buysell/my-account/')
    else:
      messages.error(request, 'The item was not posted by you.')
      return HttpResponseRedirect('/buysell/my-account/')

def dump(obj):
  for attr in dir(obj):
    print "obj.%s = %s" % (attr, getattr(obj, attr))

def clean(request):
  items = ItemsForSale.objects.all()
  req = ItemsRequested.objects.all()
  tmdlta = date.timedelta(5)
  for item in items:
    if date.today() == item.expiry_date:
      msg = 'The item ' + item.item_name + ' added by you with item id ' + item.pk + ' has reached its expiry date. '
      msg += 'Kindly extend the date using \'My Account\' menu in Buy and Sell. If the expiry date isn\'t extended, '
      msg += 'the item will be removed from database in 5 days.'
      receiver = item.email
      subject = 'Expiry date reached'
      try:
        send_mail(subject, msg, 'buysell@iitr.ernet.in', [receiver], fail_silently = False)
      except:
        pass
    if date.today() >= expiry_date + tmdlta:
      item.delete()
  for request in req:
    if date.today() == request.expiry_date:
      msg = 'The request ' + request.item_name + ' added by you with request id ' + request.pk + ' has reached its expiry date. '
      msg += 'Kindly extend the date using \'My Account\' menu in Buy and Sell. If the expiry date isn\'t extended, '
      msg += 'the request will be removed from database in 5 days.'
      receiver = item.email
      subject = 'Expiry date reached'
      try:
        send_mail(subject, msg, 'buysell@iitr.ernet.in', [receiver], fail_silently = False)
      except:
        pass
    if date.today() >= expiry_date + tmdlta:
      request.delete()

def requested_item_details(request,item_id):
  try:
    item=ItemsRequested.objects.get(pk=item_id)
  except:
    messages.error(request,'The request has been deleted/does not exist.')
    return HttpResponseRedirect('/buysell/')
  user=request.user.username
  item_user=item.user.username
  self_flag = 0
  if item and user==item_user:
    self_flag = 1
  return render_to_response('buysell/requested-item-details.html', {'rows_request': item, 'self_flag':self_flag,}, context_instance=RequestContext(request) )

def buy_item_details(request,item_id):
  try:
    item=ItemsForSale.objects.get(pk=item_id)
  except:
    messages.error(request , 'The item has been deleted/does not exist.')
    return HttpResponseRedirect('/buysell/')
  mc=item.category
  sc=item.sub_category
  mcn=''
  scn=''
  if mc:
    if mc == 'EL':
      mcn='Electronics'
    elif mc == 'BK':
      mcn='Books'
    elif mc == 'MS':
      mcn='Miscellaneous'
  else:
    mcn='Recent'
  if sc:
    if sc == 'LP':
      scn='Computer Accessories'
    elif sc == 'MO':
      scn='Mobile Accessories'
    elif sc == 'OT':
      scn='Other'
    elif sc == 'ED':
      scn='Education'
    elif sc == 'CS':
      scn='Course Books'
    elif sc == 'FC':
      scn='Fiction'
    elif sc == 'TR':
      scn='Trunks'
    elif sc == 'BC':
      scn='Bicycle'
  else:
    scn=''
  user=request.user.username
  item_user=item.user.username
  self_flag=0
  if item and user==item_user:
    self_flag=1
  return render_to_response('buysell/buy-item-details.html', {'rows': item, 'self_flag':self_flag,'sc':sc,'mc':mc,'mcn':mcn,'scn':scn}, context_instance=RequestContext(request) )

#for checking that item name does not contain special characters
def special_match(strg):
  pattern = r'[A-z0-9\s]'
  return bool(re.match(pattern, strg))
