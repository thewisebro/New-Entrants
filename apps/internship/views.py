from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.template import RequestContext 
from django.db.models import Q
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
from placement.models import InternshipInformation, ProjectInformation, EducationalDetails
from placement.policy import current_session_year
from placement.utils import get_resume_binary
from internship.utils import handle_exc

from django.conf import settings

# Permission denied page. User will be redirected to this page if he fails the user_passes_test.
login_url = '/internship/'
l=logging.getLogger('internship')
@login_required
def index(request):
  """
  Home Page
  """
  try:
    l.info(request.user.username +': tried to view Home page')
    try:
      student = request.user.student
    except:
      if request.user.groups.filter(name = 'Placement Admin').exists() :
        #In case of Placement Admin, who is not a student 
        user = request.user
        return HttpResponseRedirect(reverse('internship.views_admin.company_list_admin'))
      else :
        return render_to_response('internship/index.html', {
        'error_msg' : 'Sorry. No internship role for you.',
        }, context_instance=RequestContext(request))
    try:
      internship_person = InternshipPerson.objects.get(student = student)
    except InternshipPerson.DoesNotExist as e:
      #Adds InternshipPerson in case it is the first time this app is being opened.
      internship_person = InternshipPerson()
      internship_person.student = student
      internship_person.status = 'CLS'
      internship_person.save()
    applications = CompanyApplicationMap.objects.filter(student = internship_person, company__year__contains = current_session_year())
    selected = False
    if CompanyApplicationMap.objects.filter(student = internship_person, status = 'SEL', company__year__contains = current_session_year()).exists():
      selected = True 
    try:
      pi = StudentInfo.objects.get(student = student)
      if not pi.student.user.birth_date:
        messages.error(request, 'Please enter your date of birth')
        return HttpResponseRedirect(reverse('placement.views_profiles.personal_information'))
    except Exception as e:
      l.info(str(student)+str(e))
    if not (EducationalDetails.objects.filter(student = student, course = '10TH').exists() and EducationalDetails.objects.filter(student = student, course = '12TH').exists()) :
      messages.error(request, 'Please fill in 10th and/or 12th details to access internship')
      return HttpResponseRedirect(reverse('placement.views_profiles.educational_details'))
    return render_to_response('internship/index.html', {
      'internship_person': internship_person,
      'applications': applications,
      'selected' : selected,
      }, context_instance=RequestContext(request))
  except Exception as e:
    l.info(request.user.username +': encountered exception while viewing home page')
    l.exception(e)
    messages.error(request, 'Unknown error has occured. Please try again later. The issue has been reported.')
    return render_to_response('internship/error.html', context_instance=RequestContext(request))

@login_required
def company_open_to(request, company_id) :
  """
  Displays the name of branches for which a company is open.
  """
  try:
    import ipdb; ipdb.set_trace()
    try:
      company = Company.objects.get(id = company_id, year = current_session_year())
    except Company.DoesNotExist as e:
      l.info(request.user.username +': Company did not exist while viewing company open to')
      messages.error(request, "Company does not exist")
      return HttpResponseRedirect(reverse('internship.views_student.company_list')) 
    l.info(request.user.username +': tried to view the company_open_to view '+str(company_id))
    opento = company.open_for_disciplines.all().order_by('graduation', 'name')
    return render_to_response('internship/company_opento.html', {
        'company' : company,
        'opento' : opento
        }, context_instance = RequestContext(request))
  except Exception as e:
    l.info(request.user.username +': encountered exception while viewing company open to for '+str(company_id))
    l.exception(e)
    return handle_exc(e, request)

@login_required
def company_info(request, company_id) :
  """
  Shows the details of a Company
  """
  try:
    l.info(request.user.username +': Tried to view details of the company with compant id '+str(company_id))
    year = current_session_year()
    try:
      company = Company.objects.get(id = company_id, year = year)
    except Company.DoesNotExist as e:
      l.info(request.user.username +': The company did not exist with id '+str(company_id))
      return render_to_response('internship/generic_locked.html', {
        'error_msg' : 'Company does not exist.',
        }, context_instance = RequestContext(request))
    form = forms.BaseModelFormFunction(Company, exclude_list = ('open_for_disciplines', 'year', 'dream'), instance = company)
    return render_to_response('internship/generic_locked.html', {
      'form' : form,
      'company': company
      }, context_instance = RequestContext(request))
  except Exception as e:
    l.info(request.user.username+' : Exception while viewing details of company with compant ID '+str(company_id))
    l.exception(e)
    return handle_exc(e, request)

@login_required
def resume(request) :
  """
  Current resume of the user.
  """
  import ipdb; ipdb.set_trace()
  try:
    l.info(request.user.username +': Tried to view his resume')
    student = request.user.student 
    pdf = get_resume_binary(RequestContext(request), student, 'VER', photo_required = True)
    if pdf['err'] :
      l.info(request.user.username +': Tried to view his resume')
      return HttpResponse('Error in pdf generation')
    response = HttpResponse(pdf['content'], content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=Resume.pdf'
    response['Content-Length'] = len(pdf['content'])
    return response
  except Exception as e:
    l.info(request.user.username +': encountered exception while viewing his resume')
    l.exception(e)
    return handle_exc(e, request)


@login_required
@user_passes_test(lambda u: u.groups.filter(name='Placement Verify').count() != 0, login_url='/nucleus/login/')
def resume_to_verify(request, enrollment_no) :
  """
  Shows the resume of a student to the user Verify.
  """
  try:
    l.info(request.user.username +': tried viewing resume for verifying')
    student = Student.objects.get(user__username=enrollment_no)
    pdf = get_resume_binary(RequestContext(request), student, 'VER', False)
    if pdf['err'] :
      l.info(request.user.username +': error in pdf generation')
      return HttpResponse('Error in pdf generation')
    response = HttpResponse(pdf['content'], content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=Resume_' + enrollment_no + '.pdf'
    response['Content-Length'] = len(pdf['content'])
    return response
  except Exception as e:
    l.info(request.user.username +': encountered exception while viewing resume for verifying')
    l.exception(e)
    return handle_exc(e, request)
