from django.http import HttpResponse, HttpResponseRedirect, HttpRequest, Http404
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
from django.views.generic.base import TemplateView

from placement.utils import get_resume_binary
from internship.utils import handle_exc
import datetime
import os, xlwt
import logging

import cStringIO as StringIO
from internship.models import *
from internship import forms
from nucleus.models import Student, Branch, StudentInfo
from placement.models import InternshipInformation, ProjectInformation
from placement.policy import current_session_year

from django.conf import settings

# Permission denied page. User will be redirected to this page if he fails the user_passes_test.
login_url = '/internship/'
l=logging.getLogger('internship')

@login_required
def feedback_company_list(request, year = None) :
  """
  Display a list of companies for feedback. The user can view feedbacks
  for any of the company.
  """
  try:
    current_session = current_session_year()
    if not year :
      year = current_session
    else :
      year = int(year)
    if year > current_session :
      return HttpResponse('Wrong year') 
    l.info(request.user.username+" :tried to view list of companies for feedback for the year "+ str(year))
    #companies = Company.objects.filter(year = year)
    #counts = []
    #for company in companies :
    #  counts.append(Feedback.objects.filter(year = year, company_name = company.name_of_company).count())
    feedbacks = Feedback.objects.values('company_name').annotate(count = Count('company_name')).filter(year = year)
    session = str(year) + '-' + str(year+1)
    year_next = year + 1
    year_pervious = year - 1
    if year_next > current_session :
      show_next = False
    else :
      show_next = True
    return render_to_response('internship/feedback_company_list.html', {
      'show_next' : show_next,
      'session' : session,
      'year' : year,
      'year_next' : year_next,
      'year_previous' : year_pervious,
      'feedbacks' : feedbacks,
      }, context_instance = RequestContext(request))
  except Exception as e:
    l.info(request.user.username +': encountered exception when viewing list of companies for feedback')
    l.exception(e)
    return handle_exc(e, request)


@login_required
def company_feedback(request, year, company_name) :
  """
  Display feedback of a particular company.
  """
  try:
    feedback_list = Feedback.objects.filter(year = year, company_name = company_name).order_by('-date')
    session = str(year) + '-' + str(int(year)+1)
    paginator = Paginator(feedback_list, 10)
    page = request.GET.get('page')
    l.info(request.user.username+' tried to view feedback for '+company_name);
    if not page:
      page = 1 
    try:
      feedbacks = paginator.page(page)
    except PageNotAnInteger:
      feedbacks = paginator.page(1)
    except EmptyPage:
      feedbacks = paginator.page(paginator.num_pages)
    return render_to_response('internship/company_feedback.html', {
        'session' : session,
        'feedbacks' : feedbacks,
        'company_name' : company_name,
        }, context_instance = RequestContext(request))
  except Exception as e:
    l.info(request.user.username +': encountered an exception while viewing feedback for'+company_name)
    l.exception(e)
    return handle_exc(e, request)


@login_required
def feedback(request) :
  """
  Take feedback about a company from the user.
  """
  try:
    l.info(request.user.username+': Giving feedback for a company.')
    student = request.user.student
    if request.method == 'POST' :
      form = forms.Feedback(request.POST)
      companies = []
      for company in Company.objects.filter(year = current_session_year()) :
        companies.append((company.name_of_company, company.name_of_company))
      form.fields['company_name'].choices = companies
      if form.is_valid() :
        feedback_text = ''
        for i in range(1,9) :
          if form.cleaned_data['feedback'+str(i)] :
            feedback_text = feedback_text + '<p class="feedback_question">' + IC.FEEDBACK_QUESTIONS[i-1] + '</p>'
            feedback_text = feedback_text + '<p class="feedback_answer">' + form.cleaned_data['feedback'+str(i)] + '</p>'
        feedback_text = feedback_text.replace('\n',' ').replace('\r','').replace('\t',' ')
        company_name = form.cleaned_data['company_name']
        feedback = Feedback(enrollment_no = student.user.username,
                            person_name = student.user.name,
                            discipline_name = student.branch.name,
                            department_name = student.branch.get_department_display(),
                            company_name = company_name,
                            feedback = feedback_text,
                            date = datetime.datetime.now(),
                            year = current_session_year(),
                            )
        feedback.save()
        l.info(request.user.username+': Gave feedback for a company - '+str(company_name))
        messages.success(request, "Feedback submitted")
        return HttpResponseRedirect('/internship/feedback/'+str(current_session_year())+'/company/'+form.cleaned_data['company_name']+'/')
      else:
        messages.error(request, form.errors, extra_tags='form_error')
    else :
      form = forms.Feedback()
    for i in range(1,9) :
      form.fields['feedback'+str(i)].label=IC.FEEDBACK_QUESTIONS[i-1]
    companies =[]
    for company in Company.objects.filter(year = current_session_year()) :
      companies.append((company.name_of_company, company.name_of_company))
    form.fields['company_name'].choices = companies
    return render_to_response('internship/feedback_add.html', {
        'form' : form,
        'action' : '/internship/feedback/add/'
        }, context_instance = RequestContext(request))
  except Exception as e:
      l.info(request.user.username +': encountered exception while giving feedback')
      l.exception(e)
      return handle_exc(e, request)

@login_required
def feedback_as_pdf(request, feedback_id) :
  """
  Return a pdf file containing a particular feedback.
  """
  try:
    l.info(request.user.username+' :tried to view the feedback with feedback id: '+str(feedback_id))
    try:
      feedback = Feedback.objects.get(id = feedback_id)
    except Feedback.DoesNotExist as e:
      l.info('feedback with given id did not exist')
      return 'Feedback does not exist'
    session = str(feedback.year) + '-' + str(feedback.year+1)[2:4]
    # TODO : Use proper formatting
    html  = render_to_string('internship/feedback.html',
                           { 'pagesize' : 'A4',
                             'session' : session,
                             'feedback' : feedback,
                             },
                           context_instance = RequestContext(request))
    result = StringIO.StringIO()
    pdf = pisa.pisaDocument(StringIO.StringIO(html.encode('UTF-8')), result)
    if pdf.err :
      return HttpResponse('An error occured while generating the pdf file.')
      l.info('An eroor occured while generating the pdf file')
    response = HttpResponse(result.getvalue(), content_type='application/pdf')
    filename = feedback.company_name + '_' + feedback.person_name + '_InternshipFeedback_' + session
    response['Content-Disposition'] = 'attachment; filename=' + filename + '.pdf'
    response['Content-Length'] = len(result.getvalue())
    return response
  except Exception as e:
      l.info(request.user.username +': encountered exception while viewing feedback as pdf')
      l.exception(e)
      return handle_exc(e, request)

@login_required
def feedback_company_as_pdf(request, company_name) :
  """
  Return a pdf file containing a particular feedback.
  """
  try:
    l.info(request.user.username+' :tried to view the feedback pdf of '+str(company_name))
    year = current_session_year()
    feedbacks = Feedback.objects.filter(year = year, company_name = company_name).order_by('-date')
    session = str(year) + '-' + str(year+1)[2:4]
    # TODO : Use proper formatting
    html  = render_to_string('internship/feedback_company.html',
                           { 'pagesize' : 'A4',
                             'session' : session,
                             'company_name' : company_name,
                             'feedbacks' : feedbacks,
                             },
                           context_instance = RequestContext(request))
    result = StringIO.StringIO()
    pdf = pisa.pisaDocument(StringIO.StringIO(html.encode('UTF-8')), result)
    if pdf.err :
      l.info(request.user.username+' : got pdf error in feedback pdf of '+str(company_name))
      return HttpResponse('An error occured while generating the pdf file.')
    response = HttpResponse(result.getvalue(), content_type='application/pdf')
    filename = company_name + '_InternshipFeedback_' + session
    response['Content-Disposition'] = 'attachment; filename=' + filename + '.pdf'
    response['Content-Length'] = len(result.getvalue())
    l.info(request.user.username+' successfully download feedback pdf of '+company_name)
    return response
  except Exception as e:
    l.info(request.user.username +': encountered exception when viewing feedback pdf of '+company_name)
    l.exception(e)
    return handle_exc(e, request) 
