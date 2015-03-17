from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.template import RequestContext 
from django.core.urlresolvers import reverse
from django.forms.models import modelformset_factory
from django.db.models import Min, Count, F
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from xhtml2pdf import pisa
from django.template.loader import render_to_string
from zipfile import ZipFile
from django.contrib import messages

import datetime
import os, xlwt
import logging

import cStringIO as StringIO
from internship.models import *
from internship import forms
from nucleus.models import Student, Branch, StudentInfo
from placement.models import InternshipInformation, ProjectInformation
from placement.policy import current_session_year
from internship.utils import handle_exc

from django.conf import settings

# Permission denied page. User will be redirected to this page if he fails the user_passes_test.
login_url = '/internship/'
l=logging.getLogger('internship')

@login_required
@user_passes_test(lambda u: u.groups.filter(name='Placement Admin').count() != 0, login_url='/nucleus/login/')
def notice_add(request) :
  """
  Add a notice (for Admin)
  """
  try:
    l.info(request.user.username+' : opened view to add a notice/form')
    if request.method == 'POST' :
      form = forms.NoticeForm(request.POST, request.FILES)
      if form.is_valid() :
        form.save()
        messages.success(request, "Notice added successfully")
        l.info(request.user.username+' :added a notice successfully')
        return HttpResponseRedirect(reverse('internship.views_notice.notice_list_admin'))
      else:
        messages.error(request, form.errors, extra_tags='form_error')
        l.info(request.user.username+' : falied to add a notice')
    else :
      form = forms.NoticeForm()
    return render_to_response('internship/notice_form.html', {
      'form' : form,
      'action' : '/internship/notice/add/'
      }, context_instance = RequestContext(request))
  except Exception as e:
    l.info(request.user.username +': encountered exception when adding a notice')
    l.exception(e)
    return handle_exc(e, request)

@login_required
@user_passes_test(lambda u: u.groups.filter(name='Placement Admin').count() != 0, login_url='/nucleus/login/')
def notice_edit(request, notice_id) :
  """
  Edit a notice (for Admin)
  """
  try:
    l.info(request.user.username +': tried to edit notice '+str(notice_id))
    try:
      notice = Notices.objects.get(pk = notice_id)
    except Notices.DoesNotExist as e:
      l.info(request.user.username +': Notice did not exist')
      return render_to_response('internship/notice_form.html', {
            'error_msg' : 'Notice does NOT exist.'
            }, context_instance = RequestContext(request))
    if request.method == 'POST' :
      form = forms.NoticeForm(request.POST, request.FILES)
      if form.is_valid() :
        form.save()
        messages.success(request, "Notice edited successfully.")
        l.info(request.user.username +': Edited notice successfully')
        return HttpResponseRedirect(reverse('internship.views_notice.notice_list_admin'))
      else:
        messages.error(request, form.errors, extra_tags='form_error')
        l.info(request.user.username +': Form error while adding notice')
    else :
      form = forms.NoticeForm(instance = notice)
    return render_to_response('internship/notice_form.html', {
        'form' : form,
        'action' : '/internship/notice/add/'
        }, context_instance = RequestContext(request))
  except Exception as e:
    l.info(request.user.username +': encountered exception when editing a notice.')
    l.exception(e)
    return handle_exc(e, request)

@login_required
@user_passes_test(lambda u: u.groups.filter(name='Placement Admin').count() != 0, login_url='/nucleus/login/')
def notice_delete(request, notice_id) :
  """
  Delete a notice (for Admin)
  """
  try:
    l.info(request.user.username +': tried to delete a notice '+str(notice_id))
    try:
      notice = Notices.objects.get(pk = notice_id)
    except Notices.DoesNotExist as e:
      l.info(request.user.username +': encountered exception as the notice admin tried to delete did not exist')
      return render_to_response('internship/notice.html', {
          'error_msg' : 'Notice does NOT exist.'
          }, context_instance = RequestContext(request))
    notice.delete()
    messages.success(request, "Notice deleted successfully")
    l.info(request.user.username+' :Notice deleted successfully')
    return HttpResponseRedirect('/internship/notices/admin/')
  except Exception as e:
    l.info(request.user.username +': encountered exception when deleting a notice.')
    l.exception(e)
    return handle_exc(e, request)

@login_required
def notice_list(request) :
  """
  View list of notices
  """
  try:
    l.info(request.user.username+' : tried to view the list of notices')
    notice_list = Notices.objects.all()
    paginator = Paginator(notice_list, 10)
    page = request.GET.get('page')
    if not page:
      page = 1
    try:
      notices = paginator.page(page)
    except PageNotAnInteger:
      notices = paginator.page(1)
    except EmptyPage:
      notices = paginator.page(paginator.num_pages)
    return render_to_response('internship/notice_list.html', {
        'notices' : notices,
        }, context_instance = RequestContext(request))
  except Exception as e:
    l.info(request.user.username +': encountered exception when viewing notice list.')
    l.exception(e)
    return handle_exc(e, request)

"""
@login_required
def notice_archive(request) :  
  View list of notices
  notice_list = Notices.objects.filter(date_of_expiry__lte=datetime.date.today())
  paginator = Paginator(notice_list, 10)
  page = request.GET.get('page')
  if not page:
    page = 1 
  try:
    notices = paginator.page(page)
  except PageNotAnInteger:
    notices = paginator.page(1)
  except EmptyPage:
    notices = paginator.page(paginator.num_pages)
  return render_to_response('internship/notice_list.html', {
      'notices' : notices,
      'archive': True,
      }, context_instance = RequestContext(request))
"""

@login_required
@user_passes_test(lambda u: u.groups.filter(name='Placement Admin').count() != 0, login_url='/nucleus/login/')
def notice_list_admin(request) :
  """
  View list of notices
  """
  try:
    l.info(request.user.username+' :tried to view list of notices(admin)')
    notice_list = Notices.objects.filter()
    paginator = Paginator(notice_list, 10)
    page = request.GET.get('page')
    if not page:
      page = 1 
    try:
      notices = paginator.page(page)
    except PageNotAnInteger:
      notices = paginator.page(1)
      l.info(request.user.username +': encountered exception as page number was not an integer')
    except EmptyPage:
      notices = paginator.page(paginator.num_pages)
      l.info(request.user.username +': encountered exception as the page he requested was an empty page')
    return render_to_response('internship/notices_admin.html', {
        'notices' : notices,
        }, context_instance = RequestContext(request))
  except Exception as e:
    l.info(request.user.username +': encountered exception when viewing notice list(admin).')
    l.exception(e)
    return handle_exc(e, request)

@login_required
def notice_view(request, notice_id) :
  """
  Viewing a particular notice
  """
  try: 
    l.info(request.user.username +': Viewing notice list.')
    try:
      notice = Notices.objects.get(pk = notice_id)
    except Notices.DoesNotExist as e:
      l.info(request.user.username +': encountered exception as the notice did not exist with id '+str(notice_id))
      l.exception(e)
      return render_to_response('internship/notice.html', {
        'error_msg' : 'Notice does NOT exist.'
        }, context_instance = RequestContext(request))
    return render_to_response('internship/notice.html', {
      'notice' : notice,
      }, context_instance = RequestContext(request))
  except Exception as e:
    l.info(request.user.username +': admin encountered exception when viewing list of notices')
    l.exception(e)
    return handle_exc(e, request)



