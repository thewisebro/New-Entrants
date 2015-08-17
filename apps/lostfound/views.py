import os
import logging
from datetime import date, datetime, timedelta

from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from django.template import RequestContext
from django.core import serializers
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.html import escape
from django.conf import settings

from lostfound.models import *
from lostfound.forms import BaseModelFormFunction
# from api.forms import *
from lostfound.constants import *
from notifications.models import Notification

logger = logging.getLogger('lostfound')

@login_required
def index(request):
  logger.info(request.user.username+": in homepage.")
  user = request.user

  data_lost = LostItems.items.order_by('-pk').all()[:3]
  data_found = FoundItems.items.order_by('-pk').all()[:3]

  qryst_lost = LostItems.items.filter(user__username=user.username)
  lost_count = qryst_lost.filter(status = 'Item not found').count()
  qryst_found = FoundItems.items.filter(user__username = user.username)
  found_count = qryst_found.filter(status = 'Owner not found').count()

  dictionary = {
     'data_lost':data_lost,
     'data_found':data_found,
     'lost_count':lost_count,
     'found_count':found_count
    }

  return render_to_response('lostfound/home.html', dictionary, context_instance=RequestContext(request) )


def lost(request):
  logger.info(request.user.username+": entered lost")
  contact = request.user.contact_no
  user = request.user
  email = user.email

  if request.method == 'POST':
    form = BaseModelFormFunction(LostItems , ['user', 'status'], data=request.POST)

    date_lost = request.POST['date']
    date_lost = datetime.strptime(date_lost, "%d-%m-%Y")
    date_check = date_lost <= datetime.now()
    if form.is_valid() and date_check:
      new_entry = form.save(commit=False)
      if not _check_words_to_ignore(new_entry.item_lost):
        msg = 'Lostfound:' + request.user.username + ':' + new_entry.item_lost + " Please block."
        send_mail('Lostfound Spam', msg, 'lostfound@iitr.ernet.in', ['img.iitr.img@gmail.com'], fail_silently = False)
        del new_entry
        return HttpResponseRedirect('/logout/')
      new_entry.user = request.user
      new_entry.status = 'Item not found'
      try :
        new_entry.save()
      except Exception as e:
        messages.error(request, 'Error occured and reported.')
        logger.info(request.user.username + ': error in saving item lost.')
        logger.info(e)
        return HttpResponseRedirect('/lostfound/')
      else:
        messages.success(request, 'Item added.')
        logger.info(request.user.username + ': lost item saved.')
        return HttpResponseRedirect('/lostfound/view-item/lost/'+ str(new_entry.pk))
    else:
      if not date_check:
        messages.error(request, 'Future dates are not allowed.')
      else:
        messages.error(request, 'Please fill the form correctly.')

  else:
    form = BaseModelFormFunction(LostItems , ['user', 'status'])

  return render_to_response('lostfound/report_lost.html', { 'form': form,'email':email,'contact':contact}, context_instance=RequestContext(request) )


@login_required
def found(request):
  logger.info(request.user.username+": entered found")
  contact = request.user.contact_no
  user = request.user
  email = user.email


  if request.method == 'POST':
    form = BaseModelFormFunction(FoundItems , ['user', 'status'], data=request.POST)

    date_found = request.POST['date']
    date_found = datetime.strptime(date_found, "%d-%m-%Y")
    date_check = date_found <= datetime.now()

    if form.is_valid() and date_check:
      new_entry = form.save(commit=False)
      if not _check_words_to_ignore(new_entry.item_found):
        msg = 'Lostfound:' + request.user.username + ':' + new_entry.item_found + ' Please block.'
        send_mail('Lostfound Spam', msg, 'lostfound@iitr.ernet.in', ['img.iitr.img@gmail.com'], fail_silently = False)
        del new_entry
        return HttpResponseRedirect('/logout/')
      new_entry.user = request.user
      new_entry.status = 'Owner not found'
      try:
        new_entry.save()
      except Exception as e:
        messages.error(request, 'Error occured and reported.')
        logger.info(request.user.username + ': error in saving item found.')
        logger.info(e)
        return HttpResponseRedirect('/lostfound/')
      else:
        messages.success(request, 'Item added.')
        logger.info(request.user.username + ': saved found item')
        return HttpResponseRedirect('/lostfound/view-item/found/'+ str(new_entry.pk))
    else:
      if not date_check:
        messages.error(request, 'Future dates not allowed')
      else:
        messages.error(request, 'Please fill the form correctly!')
      form = BaseModelFormFunction(FoundItems , ['user', 'status'], data=request.POST)

  else:
    form = BaseModelFormFunction(FoundItems , ['user', 'status'])
  return render_to_response('lostfound/report_found.html', { 'form': form,'email':email,'contact':contact}, context_instance=RequestContext(request) )


def viewItem(request, category, pk_id):
  logger.info(request.user.username+": entered viewItem with category " + category + " and pk " + pk_id)
  if category == 'lost':
    try:
      result = LostItems.items.get(pk = pk_id)           #query from searchbar
    except LostItems.DoesNotExist:
      logger.info(request.user.username+": allItems/" + category + " pk = " + pk_id + ": Item not found")
      raise Http404
    template='lostfound/all_lost_items.html'
    if result.user.username == request.user.username:
      mail_flag = 0
    else:
      mail_flag = 1
    if not result:
      messages.error(request, 'No item found.')
      HttpResponseRedirect('/lostfound/')
    return render_to_response(template, { 'mail_flag':mail_flag, 'query': result}, context_instance=RequestContext(request))
  if category == 'found':
    try:
      result = FoundItems.items.get(pk = pk_id)           #query from searchbar
    except FoundItems.DoesNotExist:
      logger.info(request.user.username+": allItems/" + category + " pk = " + pk_id + ": Item not found")
      raise Http404
    template='lostfound/all_found_items.html'
    if result.user.username == request.user.username:
      mail_flag = 0
    else:
      mail_flag = 1
    if not result:
      messages.error(request, 'No item found.')
      HttpResponseRedirect('/lostfound/')
    return render_to_response(template, { 'mail_flag':mail_flag, 'query': result}, context_instance=RequestContext(request) )


@login_required
def allItems(request, category, pk=None):
  logger.info(request.user.username+": entered allItems with category " + category)
  if category == 'lost':
    table_data = LostItems.items.order_by('-pk')
    title = 'Item Lost'
    found_flag = 0
    template='lostfound/all_lost_items.html'
  if category == 'found':
    table_data = FoundItems.items.order_by('-pk')
    title = 'Item Found'
    found_flag =1
    template='lostfound/all_found_items.html'
  if not table_data:
    messages.error(request, 'No Items Found.')
    HttpResponseRedirect('/lostfound/')
  paginator = Paginator(table_data, 20)
  page = request.GET.get('page', 1)
  page_list = _get_page_list(page, paginator.num_pages, 20)
  try:
    table_data = paginator.page(page)
  except PageNotAnInteger:
    logger.info(request.user.username+": pagination error PageNotAnInteger")
    table_data = paginator.page(1)
  except EmptyPage:
    logger.info(request.user.username+": pagination error EmptyPage")
    table_data = paginator.page(paginator.num_pages)
  if pk is not None:
    pk = int(pk)
    if category == 'lost':
      try:
        obj = LostItems.items.get(pk=pk)
      except LostItems.DoesNotExist:
        logger.info(request.user.username+": allItems/" + category + " pk = " + str(pk) + ": Item not found")
        raise Http404

    elif category == 'found':
      try:
        obj = FoundItems.items.get(pk=pk)
      except FoundItems.DoesNotExist:
        logger.info(request.user.username+": allItems/" + category + " pk = " + str(pk) + ": Item not found")
        raise Http404

        obj = FoundItems.items.get(pk=pk)
    else:
      # Shouldn't happen
      raise Http404

  dic = {
    'table_data':table_data,
    'title':title,
    'found_flag':found_flag,
    'page_list':page_list,
    'key':pk,
    'paginator':paginator
  }
  return render_to_response(template, dic, context_instance=RequestContext(request))

@login_required
def account(request, category):
  logger.info(request.user.username+": entered account")
  username = request.user.username
  qryst_lost = LostItems.items.filter(user__username = username)
  qryst_lost_notfound = qryst_lost.filter(status = 'Item not found')
  qryst_found = FoundItems.items.filter(user__username = username)
  qryst_found_notfound = qryst_found.filter(status = 'Owner not found')
  lost_count = qryst_lost_notfound.count()
  found_count = qryst_found_notfound.count()
  mail_flag=1
  if category == 'lost':
    return render_to_response('lostfound/all_lost_items.html',{'qryst_lost':qryst_lost_notfound,'lost_count':lost_count,mail_flag:mail_flag},context_instance=RequestContext(request) )
  if category == 'found':
    return render_to_response('lostfound/all_found_items.html',{'qryst_found':qryst_found_notfound,'found_count':found_count,mail_flag:mail_flag},context_instance=RequestContext(request) )

@login_required
def edit(request, category, pk_id):
  logger.info(request.user.username+": entered edit with category " + category + 'and pk ' + pk_id)
  if category == 'lost':
    item = LostItems.items.get(pk = pk_id)
  if category == 'found':
    item = FoundItems.items.get(pk = pk_id)

  user = request.user
  contact = user.contact_no
  email = user.email

  if item.user.username == request.user.username:
    if category == 'lost':
      if request.method == 'POST':
        form = BaseModelFormFunction(LostItems , ['user', 'status'], data=request.POST)
        if form.is_valid():
          new_entry = form.save(commit=False)
          new_entry.pk = item.pk
          new_entry.user = request.user
          new_entry.status = 'Item not found'
          new_entry.datetime_created = item.datetime_created
          try:
            new_entry.save()
          except Exception as e:
            messages.error(request, 'Error occured and reported.')
            logger.info(request.user.username + ': error in edit - lostitems with pk ' + pk_id)
            logger.info(e)
            return HttpResponseRedirect('/lostfound/')
          else:
            messages.success(request, 'Edit Successful.')
            logger.info(request.user.username + ': save success in edit - lostitems with pk ' + pk_id)
            return HttpResponseRedirect('/lostfound/view-item/lost/'+ str(new_entry.pk))
        else:
          return render_to_response('lostfound/report_lost.html', { 'form': form, 'editFlag':1, 'item':item,'email':item.email,'contact':item.contact,'address':item.address,}, context_instance=RequestContext(request) )
      else:
        form = BaseModelFormFunction(LostItems , ['user', 'status'], instance = item)
        return render_to_response('lostfound/report_lost.html', { 'form': form, 'editFlag':1,'item':item,'email':item.email,'contact':item.contact,'address':item.address,}, context_instance=RequestContext(request) )
    if category == 'found':
      if request.method == 'POST':
        form = BaseModelFormFunction(FoundItems , ['user', 'status'], data=request.POST)
        if form.is_valid():
          new_entry = form.save(commit=False)
          new_entry.pk = item.pk
          new_entry.user = request.user
          new_entry.status = 'Owner not found'
          new_entry.datetime_created = item.datetime_created
          try:
            new_entry.save()
          except Exception as e:
            messages.error(request, 'Error occured and reported.')
            logger.info(request.user.username + ': error in edit - founditems with pk ' + pk_id)
            logger.info(e)
            return HttpResponseRedirect('/lostfound/')
          else:
            messages.success(request, 'Edit Successful.')
            logger.info(request.user.username + ': save success in edit - founditems with pk ' + pk_id)
            return HttpResponseRedirect('/lostfound/view-item/found/'+ str(new_entry.pk))
        else:
          return render_to_response('lostfound/report_found.html', { 'form': form, 'editFlag':1, 'item':item,'email':item.email,'address':item.address,'contact':item.contact}, context_instance=RequestContext(request) )

      else:
        form = BaseModelFormFunction(FoundItems , ['user', 'status'], instance = item)
        return render_to_response('lostfound/report_found.html', { 'form': form, 'editFlag':1, 'item':item,'email':item.email,'contact':contact,'address':item.address}, context_instance=RequestContext(request))
  else:
    messages.error(request, 'Item added by someone else.')
    return HttpResponseRedirect('/lostfound/')

@login_required
def sendmail(request, type_of_mail, pk_id):
  logger.info(request.user.username+": entered edit with type " + type_of_mail + 'and pk ' + pk_id)
  user = request.user
  contact = user.contact_no
  email = user.email
  app = 'lostfound'

  if type_of_mail == 'lost':
    qryst = LostItems.items.filter(pk = pk_id)
    subject = 'Your reported lost item ' + qryst[0].item_lost + ' has been reported as found!'
    msg = 'Your reported lost item ' + qryst[0].item_lost + ' has been reported as found by '
    msg += user.name
    if contact:
      msg +=  '. You can contact him/her at this number ' + str(contact)
    if email:
      msg += '. Email him at ' + str(user.email)
    if not contact and not email:
      msg += '\nThere is no contact info for ' + user.name
      msg += ' in the channel-i database.'
    template='lostfound/all_lost_items.html'

    notif_text = user.html_name() + ' found your lost item ' + escape(qryst[0].item_lost) + '. '
    if contact:
      notif_text += 'Contact him/her at ' + escape(str(contact)) + '. '
    if user.email:
      notif_text += 'Email at ' + escape(user.email) + '.'
    url = '/lostfound/view-item/lost/' + str(pk_id)
    users = [qryst[0].user]
    Notification.save_notification(app, notif_text, url, users, qryst[0])

  if type_of_mail == 'found':
    qryst = FoundItems.items.filter(pk = pk_id)
    subject = 'Your reported found item ' + qryst[0].item_found + ' has a prospective owner! '
    msg = 'Your reported found item ' + qryst[0].item_found + ' has claimed by '
    msg += user.name
    if contact:
      msg +=  '. You can contact him/her at this number ' + str(contact)
    if email:
      msg += '. Email him at ' + str(user.email)
    if not contact and not email:
      msg += '\nThere is no contact info for ' + user.name
      msg += ' in the channel-i database.'
    template='lostfound/all_found_items.html'

    notif_text = user.html_name() + ' has claimed your found item ' + escape(qryst[0].item_found) + '. '
    if contact:
      notif_text += 'Contact him/her at ' + escape(str(contact)) + '. '
    if user.email:
      notif_text += 'Email at ' + escape(user.email) + '.'
    url = '/lostfound/view-item/found/' + str(pk_id)
    users = [qryst[0].user]
    Notification.save_notification(app, notif_text, url, users, qryst[0])

  receiver = str(qryst[0].email)
  try:
    send_mail(subject, msg, 'lostfound@iitr.ernet.in', [receiver], fail_silently = False)
  except Exception as e:
    mail_flag = 0
    messages.error(request,'Incorrect receiver address. Email not sent.')
    logger.info(request.user.username + ': error in sendmail ' + pk_id)
    logger.info(e)
  else:
    msg = qryst[0].user.name + ' has been informed.'
    logger.info(request.user.username + ': sendmail successful to ' + qryst[0].user.name)
    messages.success(request, escape(msg))
    mail_flag = 1
  return render_to_response(template, {'query':qryst[0], 'mail_flag':mail_flag}, context_instance = RequestContext(request) )

@login_required
def deleteEntry(request, category, pk_id):
  logger.info(request.user.username + ': entered deleteEntry with category ' + category + '.')
  app = 'lostfound'
  if category == "lost":
    item = LostItems.items.get(pk = pk_id)
    Notification.delete_notification(app, item)
    if item.user.username == request.user.username:
      try:
        item.delete()
      except Exception as e:
        messages.error(request, 'Error occured and reported.')
        logger.info(request.user.username + ': error in delete lost with pk ' + pk_id)
        logger.info(e)
      else:
        messages.success(request, 'Item successfully deleted.')
        logger.info(request.user.username + ': deleted successfully lost with pk ' + pk_id)
    else:
      messages.error(request, 'You can not delete items added by others.')
    return HttpResponseRedirect('/lostfound/')
  elif category == "found":
    item = FoundItems.items.get(pk = pk_id)
    Notification.delete_notification(app, item)
    if item.user.username == request.user.username:
      try:
        item.delete()
      except Exception as e:
        messages.error(request, 'Error occured and reported.')
        logger.info(request.user.username + ': error in delete found with pk  ' + pk_id)
        logger.info(e)
      else:
        messages.success(request, 'Item successfully deleted.')
        logger.info(request.user.username + ': deleted successfully found with pk ' + pk_id)
    else:
      messages.error(request, 'You can not delete items added by others.')
    return HttpResponseRedirect('/lostfound/')

@login_required
def search(request, category, st):
  logger.info(request.user.username + ': entered deleteEntry with category ' + category + ' and str ' + st)
  if category == 'lost':
    table_data = LostItems.items.filter(item_lost__icontains = st)
    title = 'Item Lost'
    template = 'lostfound/all_lost_items.html'
  if category == 'found':
    table_data = FoundItems.items.filter(item_found__icontains = st)
    title = 'Item Found'
    template = 'lostfound/all_found_items.html'
  if not table_data:
    messages.error(request, 'No Items Found.')
    return HttpResponseRedirect('/lostfound/')
  paginator = Paginator(table_data, 10)
  page = request.GET.get('page', 1)
  try:
    table_data = paginator.page(page)
  except PageNotAnInteger:
    table_data = paginator.page(1)
  except EmptyPage:
    table_data = paginator.page(paginator.num_pages)
  dic = {'table_data':table_data, 'title':title,'page_list':paginator.page_range,}
  return render_to_response(template, dic, context_instance=RequestContext(request))

@login_required
def status(request, category, pk_id):
  logger.info(request.user.username + ': entered status with category ' + category + ' and pk ' + pk_id)
  if category == 'lost':
    item = LostItems.items.get(pk = pk_id)
  if category == 'found':
    item = FoundItems.items.get(pk = pk_id)

  if item.user.username == request.user.username:
    if category == 'lost':
      item.status = 'Item found'
      try:
        item.save()
      except Exception as e:
        messages.error(request, 'Error occured while saving. Reported.')
        logger.info(request.user.username + ': error change status of lost item with pk  ' + pk_id)
        logger.info(e)
        return HttpResponseRedirect('/lostfound/')
      else:
        messages.success(request, 'Edit Successful.')
        logger.info(request.user.username + ': successfully changed status of lost item with pk ' + pk_id)
        return HttpResponseRedirect('/lostfound/')
    if category == 'found':
      item.status = 'Owner found'
      try:
        item.save()
      except Exception as e:
        messages.error(request, 'Error occured while saving. Reported.')
        logger.info(request.user.username + ': error change status of found item with pk  ' + pk_id)
        logger.info(e)
        return HttpResponseRedirect('/lostfound/')
      else:
        messages.success(request, 'Edit Successful.')
        logger.info(request.user.username + ': successfully changed status of lost item with pk ' + pk_id)
        return HttpResponseRedirect('/lostfound/')
  else:
    messages.error(request, 'You cannot edit item added by someone else.')

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

def _check_words_to_ignore(st):
  f = open(settings.PROJECT_ROOT + '/apps/lostfound/wordstoignore.txt', 'r')
  words = [line[:-1] for line in f]
  f.close()
  st = st.split(' ')
  for s in st:
    if s in words:
      return False
  return True
