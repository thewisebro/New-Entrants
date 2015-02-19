from django.http import HttpResponse, HttpResponseRedirect, HttpRequest, Http404
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
from django.views.generic.base import TemplateView

import datetime
import os, xlwt
import logging

import cStringIO as StringIO
from internship.models import *
from internship import forms 
from nucleus.models import Student, Branch, StudentInfo
from placement.models import InternshipInformation, ProjectInformation
from placement.policy import current_session_year
from placement.utils import handle_exc
from django.conf import settings

# Permission denied page. User will be redirected to this page if he fails the user_passes_test.
login_url = '/internship/'
l=logging.getLogger('internship')

@login_required
def results_company_list(request, year = None) :
  """
  View list of companies for the purpose of getting the results for
  a particular year.
  """
  try:
    current_session = current_session_year()
    if not year :
      year = current_session
    else :
      year = int(year) # unicode is given by the link
    l.info(request.user.username+' : tried to view list of companies for the purpose of getting the results for '+ str(year))
    # Show those companies only which have declared results i.e. have selected at least one student.
    results = ResultsNew.objects.filter(company__year__exact = year).values_list('company')
    results = results.values_list('company__name_of_company', 'company').annotate(placed_count = Count('company')).order_by('company__name_of_company')
    # get the year of the oldest result
    year_min = ResultsNew.objects.aggregate(min = Min('company__year'))['min']
    if not year_min :
      year_min = current_session
    sessions = []
    for i in range(year_min, current_session):
      sessions.append(str(i) + '-' + str(i+1)[2:4])
    # years_list for displaying on the top. It is in the form
    # [(2010,'2010-11'), (2011,'2011-12')]
    years_list = zip(range(year_min, current_session), sessions)
    session = str(year) + '-' + str(year+1)[2:4]
    return render_to_response('internship/results_list.html', {
      'years_list' : years_list,
      'session' : session,
      'year' : year,
      'list_of' : 'Company',
      'list' : results
      }, context_instance = RequestContext(request))
  except Exception as e:
      l.info(request.user.username +': encountered exception while viewing list of companies.')
      l.exception(e)
      return handle_exc(e, request)

@login_required
def company_results(request, company_id, year = None) :
  """
  View results of a company for a particular year.
  """
  l.info(request.user.username+' : tried to view results of company with company_id '+str(company_id))
  try:
    if not year :
      year = current_session_year()
    else :
      year = int(year) # the link gives unicode
    try:
      company = Company.objects.get(pk = company_id)
    except Exception as e:
      return direct_to_template(request, template="404.html")
    results = ResultsNew.objects.filter(company = company)
#    degrees = []
#    for result in results :
     # Try to get the degree of the person. Do not care if the data is missing.
#      try :
#        degrees.append(Student.objects.get(user__username = result.person.user.username).branch.get_degree_display())
#      except Student.DoesNotExist :
#        degrees.append(None)
#    results = zip(results, degrees)
    session = str(year) + '-' + str(year+1)[2:4]
    # TODO : Display Course of the person in place of the department
    return render_to_response('internship/results_view_company.html', {
      'results_for' : company.name_of_company,
      'session' : session,
      'results' : results
      }, context_instance = RequestContext(request))
  except Exception as e:
    l.info(request.user.username +': encountered exception while viewing results for comapny with company_id '+str(company_id))
    l.exception(e)
    return handle_exc(e, request)

  
@login_required
def results_discipline_list(request, year = None) :
  """
  View list of disciplines for the purpose of getting the results for
  a particular year.
  """
  try:
    current_session = current_session_year()
    if not year :
      year = current_session
    else :
      year = int(year) # unicode is given by the link
    l.info(request.user.username+' : tried to view list of disciplines for the purpose of getting the results for '+str(year))
    # TODO : How to display branches for UG/PG/DUAL etc?
    # Should an option be given to select degree??
    # For the time being, display all the Branch rows.
    results = ResultsNew.objects.filter(company__year__exact = year)
    total_placements = results.count()
    results = results.values_list('person__branch__code', 'person__branch__name').annotate(placed_count = Count('person__branch')).order_by('person__branch__name')
    # get the year of the oldest result
    year_min = ResultsNew.objects.aggregate(min = Min('company__year'))['min']
    if not year_min :
      year_min = current_session
    # count of students placed in a branch
    sessions = []
    for i in range(year_min, current_session):
      sessions.append(str(i) + '-' + str(i+1)[2:4])
    # years_list for displaying on the top. It is in the form
    # [(2010,'2010-11'), (2011,'2011-12')]
    years_list = zip(range(year_min, current_session), sessions)
    session = str(year) + '-' + str(year+1)[2:4]
    return render_to_response('internship/results_list.html', {
      'years_list' : years_list,
      'session' : session,
      'year' : year,
      'list_of' : 'Branch',
      'list' : results
      }, context_instance = RequestContext(request))
  except Exception as e:
    l.info(request.user.username +': encountered exception while viewing getting list of disciplines for results')
    l.exception(e)
    return handle_exc(e, request)

@login_required
def branch_results(request, discipline_name, year = None) :
  """
  View results of a branch for a particular year.
  """
  try:
    if not year :
      year = current_session_year()
    else :
      year = int(year) # link gives year in unicode
    l.info(request.user.username+' : tried to view results of '+str(discipline_name)+' for '+str(year))
    try:
      branch = Branch.objects.get(code = discipline_name)
    except Exception as e:
      l.info(request.user.username+' : Exception while viewing results of '+str(discipline_name))
      return direct_to_template(request, template="404.html")
    results = ResultsNew.objects.filter(person__branch = branch, company__year__exact = year).order_by('person__name')
#    degrees = []
#    for result in results :
#      # Try to get the degree of the person. Do not care if the data is missing.
#      try :
#        degrees.append(Student.objects.get(user__username = result.person.user.username).branch.get_degree_display())
#      except Student.DoesNotExist :
#        degrees.append(None)
    session = str(year) + '-' + str(year+1)[2:4]
#    results = zip(results, degrees)
    # TODO : Display Course of the person in place of the department
    return render_to_response('internship/results_view_branch.html', {
      'results_for' : branch.name,
      'session' : session,
      'results' : results
      }, context_instance = RequestContext(request))
  except Exception as e:
    l.info(request.user.username +': encountered exception while viewing results of '+str(discipline_name)+' for a particular year')
    l.exception(e)
    return handle_exc(e, request)


@login_required
def branch_results_company(request, discipline_name, year = None) :
  """
  View results of a branch grouped by company for a particular year.
  """
  try:
    if not year :
      year = current_session_year()
    else :
      year = int(year) # link gives year in unicode
    l.info(request.user.username +': tried to view results of '+str(discipline_name)+' for '+str(year))
    results = ResultsNew.objects.filter(company__year__exact = year)
    try:
      branch = Branch.objects.get(code = discipline_name)
    except Exception as e:
      l.info(request.user.username +': encountered an exception while getting the branch name')
      return direct_to_template(request, template="404.html")
    results = results.filter(person__branch = branch).values('company', 'company__name_of_company').order_by('company__name_of_company').annotate(placed = Count('company__name_of_company'))
    session = str(year) + '-' + str(year+1)[2:4]
    total_placed = []
    for result in results :
      total_placed.append(ResultsNew.objects.filter(company = result['company']).count())
    results = zip(results, total_placed)
    # TODO : Display Course of the person in place of the department
    return render_to_response('internship/results_view_branch_company.html', {
      'results_for' : branch.name,
      'session' : session,
      'results' : results
      }, context_instance = RequestContext(request))
  except Exception as e:
    l.info(request.user.username +': encountered exception while viewing results of '+str(discipline_name)+' grouped by company for a particular year')
    l.exception(e)
    return handle_exc(e, request)

@login_required
@user_passes_test(lambda u: u.groups.filter(name='Placement Admin').count() != 0, login_url='/nucleus/login/')
def declare_result(request, company_id) :
  """
  Declare results for the company.
  """
  try:
    try:
      company = Company.objects.get(id = company_id, year = current_session_year())
      l.info(request.user.username +': opened view to declare results for company '+str(company_id))
    except Company.DoesNotExist as e:
      l.info(request.user.username +': The company did not exist')
      return render_to_response('internship/company_list_admin.html', {
          'error_msg' : 'Company does NOT exist.',
          }, context_instance = RequestContext(request))
    error_msg = None
    if request.method == 'POST':
      # set status of selected application to SELECTED
      CompanyApplicationMap.objects.filter(pk__in = request.POST.getlist('selected_applications')).update(status='SEL')
      errors = []
      # create entry in Results
      for application in CompanyApplicationMap.objects.filter(pk__in = request.POST.getlist('selected_applications')) :
        internship_person = application.person
        if internship_person.is_placed == False :
          internship_person.is_placed = True
          person = application.person.person
          ResultsNew(person = person,
              company = company
              ).save()
        else :
          errors.append(internship_person.person.name)
          CompanyApplicationMap.objects.filter(person = internship_person).update(status='FIN')
        # Update InternshipPerson of the person just placed.
        internship_person.save()
      if len(errors)>0:
        error_msg = "The results of the following were not declared as they have already been selected: "
        l.info(request.user.username +': The results of the following were not declared as they have already been selected')
        error_msg += ", ".join(errors)
      else:
        l.info(request.user.username +': Results successfully declared')
        messages.success(request, 'Results declared.')
        return HttpResponseRedirect('/internship/company/')
    applications = CompanyApplicationMap.objects.filter(company = company, status = 'FIN')
    return render_to_response('internship/declare_results.html', {
          'company' : company,
          'applications' : applications,
          'error_msg' : error_msg,
          }, context_instance = RequestContext(request))
  except Exception as e:
    l.info(request.user.username +': encountered exception while declaring results for '+str(company_id))
    l.exception(e)
    return handle_exc(e, request)

@login_required
@user_passes_test(lambda u: u.groups.filter(name='Placement Admin').count() != 0, login_url='/nucleus/login/')
def drop_results(request, company_id) :
  """
  Drop some results from the results that were earlier declared for the company.
  """
  try:
    try:
      l.info(request.user.username +' : visited the page to drop results that were earlier declared for the company '+str(company_id))
      company = Company.objects.get(id = company_id, year = current_session_year())
    except Company.DoesNotExist as e:
      l.info(request.user.username +' : Company did not exist')
      return render_to_response('internship/company_list_admin.html', {
            'error_msg' : 'Company does NOT exist.',
            }, context_instance = RequestContext(request))
    error_msg = None
    errors = []
    if request.method == 'POST':
      # results which are to be dropped
      results = ResultsNew.objects.filter(person__user__username__in = request.POST.getlist('selected_results'))
      # enrollment_no of students whose results are being dropped
      enrollment_nos = results.values_list('person__user__username', flat = True)
      # Revert back the status of selected applications from SELECTED to FINALIZED
      CompanyApplicationMap.objects.filter(person__person__user__username__in = enrollment_nos).update(status='FIN')
      # Set the internship persons of these students as not placed
      InternshipPerson.objects.filter(person__user__username__in = enrollment_nos).update(is_placed = False)
      # Remove the corresponding entries form Results
      results.delete()
      messages.success(request, 'Results dropped successfully.')
      return HttpResponseRedirect('/internship/company/')
    #Use info from Results table
    results = ResultsNew.objects.filter(company = company)
    return render_to_response('internship/drop_results.html', {
          'company' : company,
          'results' : results,
          'error_msg' : error_msg,
          }, context_instance = RequestContext(request))
  except Exception as e:
    l.info(request.user.username +': encountered exception while dropping results for '+str(company_id))
    l.exception(e)
    return handle_exc(e, request)
  
@login_required
@user_passes_test(lambda u: u.groups.filter(name='Placement Admin').exists(), login_url=login_url)
def insert_result(request, company_id, branch_code = None) :
  """
  Insert results for the company.
  """
  try:
    l.info(request.user.username +' : visited the page to declare results for the company '+str(company_id)) 
    company = get_object_or_404(Company, pk = company_id, year = current_session_year() )
    if request.method == 'POST':
      students = InternshipPerson.objects.filter(pk__in = request.POST.getlist('selected_students'))
      errors = []
      for internship_person in students :
        if internship_person.is_placed == False :
          internship_person.is_placed = True
          person = internship_person.person
          CompanyApplicationMap(person = internship_person,
                company = company,
                status = 'SEL'
                ).save()
          ResultsNew(person = person,
                company = company
                ).save()
          # Update InternshipPerson of the person just placed.
          internship_person.save()
        else :
          errors.append(internship_person.person.name)
      if len(errors)>0:
        l.info(request.user.username +' : Error while inserting results as the results have already been declared')
        error_msg = "The results of the following were not declared as they have already been selected: "
        error_msg += ", ".join(errors)
        messages.error(request, error_msg)
      else:
        l.info(request.user.username+' : Results declared successfully')
        messages.success(request, 'Results inserted successfully')
      return HttpResponseRedirect(reverse('internship.views_admin.company_list_admin'))
    elif branch_code <> None :
      branch = Branch.objects.get(pk = branch_code)
      student_list = InternshipPerson.objects.filter(person__branch = branch, status = 'OPN')
      return render_to_response('internship/insert_results.html', {
          'company' : company,
          'student_list' : student_list,
          }, context_instance = RequestContext(request))
    else :
      branches = Branch.objects.all()
      return render_to_response('internship/insert_results.html', {
          'company' : company,
          'branches' : branches,
          }, context_instance = RequestContext(request))
  except Exception as e:
    l.info(request.user.username +': encountered exception while inserting results for '+str(company_id))
    l.exception(e)
    return handle_exc(e, request)
