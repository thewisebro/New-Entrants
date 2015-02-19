from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.core.servers.basehttp import FileWrapper
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.template import RequestContext 
from django.db.models import Q
from django.http import Http404
from django.core.urlresolvers import reverse
from django.forms.models import modelformset_factory
from django.db.models import Min, Count, F
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from xhtml2pdf import pisa
from django.template.loader import render_to_string
from zipfile import ZipFile
from django.contrib import messages
from django.views.generic.base import TemplateView
from django.views.decorators.csrf import csrf_exempt

import datetime
import os, xlwt
import logging
import mimetypes
import simplejson as json

import cStringIO as StringIO
from internship.models import *
from internship import forms 
from nucleus.models import Student, Branch, StudentInfo
from placement.utils import get_resume_binary, handle_exc
from placement.models import InternshipInformation, ProjectInformation
from placement.policy import current_session_year

from django.conf import settings

# Permission denied page. User will be redirected to this page if he fails the user_passes_test.
login_url = '/internship/'
l=logging.getLogger('internship')
   
@login_required
@user_passes_test(lambda u: u.groups.filter(name='Student').count() != 0, login_url='/nucleus/login/')
def company_list(request):
  """
  Displays the list of companies to student. The student can apply to a company if that company
  is open for his discipline. He has a withdraw option if he has already applied to a company.
  The current status of the application to a company is also shown.
  """
  try:
    l.info(request.user.username + ": viewing company list.")
    companies = Company.objects.filter( year = current_session_year() )
    person = request.session.get('person')
    try:
      internship_person = InternshipPerson.objects.get(person = person)
    except InternshipPerson.DoesNotExist as e:
      l.info(request.user.username + ": viewing company list but internship_person doesnt exist.")
      return render_to_response('internship/company_list.html',{
          'error_msg': '',
          }, context_instance = RequestContext(request))
    try:
      pi = StudentInfo.objects.get(person = person)
      if not pi.birth_date:
        messages.error(request, 'Please enter your date of birth')
        return HttpResponseRedirect(reverse('placement.views_profiles.personal_information'))
    except Exception as e:
      l.info(str(person)+str(e))
    status = [] # list to store the status of the application in order of the list "companies"
    # Different status possible are
    #   1. NOT - Not applicable
    #   2. NAP - Not Applied
    #       + other status from internship.constants.COMPANY_APPLICATION_STATUS
    opencompanies = []
    avlstatus = [] #status of companies which are availabe for application by the person
    for company in companies :
        branches = company.open_for_disciplines.all()
        if company.status == 'OPN' and person.branch in company.open_for_disciplines.all(): 
          opencompanies.append(company)
          try:
            application = CompanyApplicationMap.objects.get(company = company, person = internship_person, company__year__contains = current_session_year())
            avlstatus.append(application.status)
          except:
            avlstatus.append('NAP')
        if company.status=='CLS':
          status.append('CLS')
        elif CompanyApplicationMap.objects.filter(person = internship_person, status = 'SEL', company__year__contains = current_session_year()).exists():
          status.append('SEL')
        elif person.branch in branches and internship_person.status == 'OPN' and company.status == 'OPN':  
          try:
            application = CompanyApplicationMap.objects.get(company = company, person = internship_person, company__year__contains = current_session_year())
            status.append(application.status)
          except CompanyApplicationMap.DoesNotExist as e:
            status.append('NAP')
        elif person.branch in branches and internship_person.status != 'CLS':  
          status.append(company.status)
        elif person.branch not in branches:  
          status.append('CLS')
        elif company.status=='DEC':
          status.append('DEC')
        elif company.status=='FIN':
          status.append('FIN')
        else:
          status.append('NOT')
    company_status_map = zip(companies, status)
    avl_company_status_map = zip(opencompanies, avlstatus)
    print avl_company_status_map
    return render_to_response('internship/company_list.html', {
        'company_status_map' : company_status_map,
        'avl_company_status_map': avl_company_status_map,
        'internship_person': internship_person,
        }, context_instance = RequestContext(request))
  except Exception as e:
    l.info(request.user.username + ": encountered error while listing company.")
    l.exception(e)
    return handle_exc(e, request)

@login_required
@user_passes_test(lambda u: u.groups.filter(name='Student').count() != 0, login_url='/nucleus/login/')
def apply(request, company_id) :
  """
  Applies to the specified company. Returns True if applied otherwise returns an error message.
  It is to be used via AJAX call.
  """
  try:
    year = current_session_year()
    try:
      company = Company.objects.get(id = company_id, year = year)
    except Company.DoesNotExist as e:
      return HttpResponse('Company does NOT exist.')
    person = request.session.get('person')
    try:
      internship_person = InternshipPerson.objects.get (person = person, status = 'OPN')
    except InternshipPerson.DoesNotExist as e:
      l.info ('internship person with enrollment no '+ request.user.username +' is not open.')
      return HttpResponse('You canot apply to this company')
    if CompanyApplicationMap.objects.filter(company = company, person = internship_person, company__year__contains = current_session_year()).exists():
      l.info (request.user.username +' can not apply again as he/she has already applied to company.')
      return HttpResponse("Multiple applications to the same company not allowed. This shall be reported.")
    elif InternshipPerson.objects.filter(person = person, is_placed = 'True').exists():
      l.info (request.user.username +' can not apply as he/she is already placed.')
      return HttpResponse("You can not apply to a company after getting the internship. This shall be reported.")
    elif company.status != 'OPN':
      l.info (request.user.username +' applying to closed company '+str(company.name_of_company))
      return HttpResponse("You can not apply to this company as it is closed.")
    try:
      cgpa_req = float(company.cgpa_requirements)
    except:
      cgpa_req = 0
    if cgpa_req > float(internship_person.person.cgpa):
      l.info (request.user.username +' applying to company having higher CGPA requirements.')
      return HttpResponse("You can not apply to this company as it has higher CGPA requirements.")
    else:
      branches = company.open_for_disciplines.all()
      if person.branch in branches:
        pdf = get_resume_binary(RequestContext(request), person, 'VER', False, photo_required = True)
        if pdf['err'] :
          return HttpResponse('Your resume cannot be generated. Please contact IMG immediately.')
        filepath = os.path.join(settings.MEDIA_ROOT, 'internship', 'applications', 'company'+str(company_id), str(person.user.username)+'.pdf')
        # Make sure that the parent directory of filepath exists
        parent = os.path.split(filepath)[0]
        if not os.path.exists(parent) :
          os.makedirs(parent)
        resume = open(filepath, 'w')
        resume.write(pdf['content'])
        resume.close()
        application = CompanyApplicationMap()
        application.person = internship_person
        application.company = company
        application.status = 'APP'
        application.save()
        l.info (request.user.username +' applied to company '+str(company.name_of_company))
        return HttpResponse("True")
      else:
        l.info (request.user.username +' unsuccessfully applied to company as it is not open for his/her branch- '+str(company.name_of_company))
        return HttpResponse("Your branch is not applciable to this company. This shall be reported")
  except Exception as e:
    l.info(request.user.username+ ": encountered error while applying to a company.")
    l.exception(e)
    return HttpResponse('Unknown error has occured. Please try later. The issue has been reported.')

@login_required
@user_passes_test(lambda u: u.groups.filter(name='Student').count() != 0, login_url='/nucleus/login/')
def withdraw(request, company_id) :
  """
  Withdraws application from the company. Returns True if the application was withdrawn.
  Otherwise the error message is returned. It is to be used via AJAX call.
  """
  try:
    year = current_session_year()
    try:
      company = Company.objects.get(id = company_id, year = year)
    except Company.DoesNotExist as e:
      l.info (request.user.username +': tried to withdraw from company which doesnt exist')
      return HttpResponse('Company does NOT exist')
    person = request.session.get('person')
    try:
      internship_person = InternshipPerson.objects.get(person = person, status = 'OPN')
    except InternshipPerson.DoesNotExist as e:
      l.info (request.user.username +': internship person does not exist while withdrawing company '+str(company.name_of_company))
      return HttpResponse('You cannot withdraw from this company (Error 1)')
    try:
      application = CompanyApplicationMap.objects.get (company = company, person = internship_person, company__year__contains = current_session_year())
    except CompanyApplicationMap.DoesNotExist as e:
      l.info (request.user.username +': application does not exist while withdrawing company '+str(company.name_of_company))
      return HttpResponse('You can not withdraw your application from this company')
    if not application.status == 'APP':
      # The application has been forwarded to the company.
      l.info (request.user.username +': application already finalized while withdrawing company '+str(company.name_of_company))
      return HttpResponse('You cannot withdraw your application from '+ company.name_of_company)
    elif CompanyApplicationMap.objects.filter(person = internship_person, status = 'SEL', company__year__contains = current_session_year()).exists():
      l.info (request.user.username +': person already placed while withdrawing company '+str(company.name_of_company))
      return HttpResponse('You cannot perform this action as you have already been selected in a company.')
    elif application.company.status != 'OPN':
      l.info (request.user.username +': person tried to withdraw application from Closed Company')
      return HttpResponse('You cannot perform this action as '+ company.name_of_company +' application is closed')
    filepath = os.path.join(settings.MEDIA_ROOT, 'internship', 'applications', 'company'+str(company_id), str(person.user.username)+'.pdf')
    if os.path.exists(filepath) :
      os.remove(filepath)
    application.delete()
    l.info (request.user.username +' withdrew from company '+str(company.name_of_company))
    return HttpResponse("True")
  except Exception as e:
    l.info(request.user.username+ ": encountered error while withrawal of appication.")
    l.exception(e)
    return handle_exc(e, request)

@login_required
def submitted_resume(request, company_id) :
  """
  Returns the resume submitted by the user to specific company.
  """
  try:
    person = request.session['person']
    l.info(request.user.username + ":trying to get resume submitted to a particular company.")
    filename = os.path.join(settings.MEDIA_ROOT, 'internship', 'applications', 'company'+str(company_id), str(person.user.username)+'.pdf')
    if not os.path.exists(filename) : # the user has not applied to the company
      return direct_to_template(request, template="404.html")
    wrapper = FileWrapper(file(filename))
    response = HttpResponse(wrapper, content_type=mimetypes.guess_type(filename)[0])
    response['Content-Length'] = os.path.getsize(filename)
    response['Content-Disposition'] = 'attachment; filename=Resume.pdf'
    return response
  except Exception as e:
    l.info(request.user.username + ": encountered error while getting resume submitted to a particular company.")
    l.exception(e)
    return handle_exc(e, request)

@csrf_exempt
@login_required
def set_priority(request):
  person = request.user.person
  internship_person = InternshipPerson.objects.get_or_create(person=person)[0]
  companies_applied = CompanyApplicationMap.objects.filter(person=internship_person, company__pk__in = [229,230,231,233,234])
  message=""
  for company in companies_applied:
    company_priority = CompanyPriority.objects.get_or_create(person=person,company=company.company)
  company_data = CompanyPriority.objects.filter(person=person)
  if not companies_applied:
    message = "You have not applied for any of the companies for which priority is required. In case of any discrepancy, contact IMG."
  if request.method == "POST":
    company_priority = CompanyPriority.objects.filter(person=person).delete()
    data = json.loads(request.POST.items()[0][0])
    message = ""
    is_success = True
    for priority in data:
      try:
        company = Company.objects.get(pk=priority["id"])
        company_priority = CompanyPriority.objects.get_or_create(person=person,company=company)[0]
        company_priority.priority = int(priority["priority"])+1
        company_priority.save()
      except Exception as e:
        message = "Some error occured. Please contact IMG"
        is_success = False
        l.info(request.user.username + ": encountered error while setting priority "+str(e))
    if not message:
      message = "Saved Successfully"
    json_data = json.dumps({'message':message,'is_success':is_success})
    return HttpResponse(json_data,mimetype='application/json')

  return render_to_response('internship/priority.html', {
        "data": company_data,
        "message":message,
        }, context_instance = RequestContext(request))
