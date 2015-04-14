import re, os

from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.template import RequestContext 
from django.db.models import Q

from core.forms import BaseForm, BaseModelForm
from filemanager import FileManager
from settings.common.settings import MEDIA_ROOT, NAS_MEDIA_ROOT, NAS_PUBLIC_URL

from nucleus.models import Branch, Faculty, User

from facapp.models import *
from facapp.utils import handle_exc
from facapp.forms import BooksAuthoredForm, RefereedJournalPapersForm, PhotoUploadForm, ResumeUploadForm, BaseModelFormFunction, ConfirmDeleteForm

@login_required
@user_passes_test(lambda u: u.groups.filter(name='Faculty').count() != 0)
def upload_photo(request):
  try:
    faculty = request.user.faculty
    if request.method == 'POST':
      photo_form = PhotoUploadForm(request.POST, request.FILES)
      if photo_form.is_valid():
        faculty.photo = request.FILES['photo']
        faculty.save()
        messages.success(request, 'Photo was successfully updated.')
      else:
        # To handle form errors we need to add extra_tags. Now the tag becomes 'form_error error'
        messages.error(request, photo_form.errors, extra_tags='form_error')
    return HttpResponseRedirect(reverse('facapp.views.index'))
  except Exception as e:
    return handle_exc(e, request)

@login_required
@user_passes_test(lambda u: u.groups.filter(name='Faculty').count() != 0)
def upload_resume(request):
  '''  This view function is similar to upload_photo view function.  '''
  try:
    faculty = request.user.faculty
    if request.method == 'POST':
      resume_form = ResumeUploadForm(request.POST, request.FILES)
      if resume_form.is_valid():
        faculty.resume = request.FILES['resume']
        faculty.save()
        messages.success(request, 'Resume was successfully updated.')
      else:
        messages.error(request, resume_form.errors, extra_tags='form_error')
    return HttpResponseRedirect(reverse('facapp.views.index'))
  except Exception as e:
    return handle_exc(e, request)

@login_required
@user_passes_test(lambda u: u.groups.filter(name='Faculty').count() != 0)
def website_page(request):
  ''' To show website upload link  '''
  return render(request, 'facapp/website_page.html')
  
@login_required
@user_passes_test(lambda u: u.groups.filter(name='Faculty').count() != 0)
def websitebrowser(request,path):
  if not os.path.exists(MEDIA_ROOT+'facapp/websites/'+request.user.username):
    os.chdir(MEDIA_ROOT+'facapp/websites/')
    os.mkdir(request.user.username)
    os.chdir(MEDIA_ROOT+'facapp/websites/'+request.user.username)
    os.mkdir('Website')

  fm = FileManager(MEDIA_ROOT+'facapp/websites/'+request.user.username+'/Website')
  return fm.render(request,path)

@login_required
@user_passes_test(lambda u: u.groups.filter(name__in=('Faculty','NasSpaceUser')).exists())
def faculty_filemanager(request,path):
  if not os.path.exists(NAS_MEDIA_ROOT+'facspace/'+request.user.username):
    os.chdir(NAS_MEDIA_ROOT+'facspace/')
    os.mkdir(request.user.username)

  space = FacSpace.objects.filter(user = request.user)
  if len(space):
    space = space[0].space*1024*1024
  else:
    space = 5*1024*1024
  fm = FileManager(NAS_MEDIA_ROOT+'facspace/'+request.user.username,maxfolders=500,maxspace=space,maxfilesize=space,public_url_base=NAS_PUBLIC_URL+'facspace/'+request.user.username)
  return fm.render(request,path)
