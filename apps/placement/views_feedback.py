from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.template.loader import render_to_string
from django.db.models import Min, Count
from django.views.generic.base import TemplateView

from xhtml2pdf import pisa

import cStringIO as StringIO
import logging, datetime

from django.contrib import messages

from placement import constants as PC, forms
from placement.policy import current_session_year
from placement.models import *
from placement.utils import *

l = logging.getLogger('placement')

# Permission denied page. User will be redirected to this page if he fails the user_passes_test.
login_url = '/placement/'

# IMPORTANT : Objects of Student and PlacementPerson are to be stored in session.
# These objects are used in all the templates.

@login_required
@user_passes_test(lambda u: u.groups.filter(name__in=('Student', 'Placement Admin')).exists(), login_url=login_url)
def index(request, year = None) :
  """
  Display a list of companies for feedback. The user can view feedbacks
  for any of the company.
  """
  try :
    l.info (request.user.username + ': Viewing company feedback list.')
    current_session = current_session_year()
    if not year :
      year = current_session
    else :
      year = int(year)
    feedbacks = Feedback.objects.filter(company__year__exact = year)
    total_feedbacks = feedbacks.count()
    feedbacks = feedbacks.values('company', 'company__name').annotate(count = Count('company')).order_by('company__name')
    year_min = Feedback.objects.aggregate(min = Min('company__year'))['min']
    status = None
    if request.user.groups.filter(name = 'Student').exists() :
      student = request.session['student']
      status = request.session['plac_person'].status
    sessions = []
    if not year_min :
      year_min = current_session
    for i in range(year_min, current_session):
      sessions.append(str(i) + '-' + str(i+1)[2:4])
    # years_list for displaying on the top. It is in the form
    # [(2010,'2010-11'), (2011,'2011-12')]
    years_list = zip(range(year_min, current_session), sessions)
    # TODO : Display a list of years so that the user can browse previous
    # years' feedbacks.
    session = str(year) + '-' + str(year+1)
    return render_to_response('placement/feedback_company_list.html', {
        'session' : session,
        'feedbacks' : feedbacks,
        'status' : status,
        'total_feedbacks' : total_feedbacks,
        'years_list' : years_list,
        'year' : year,
        'current_year' : current_session,
        }, context_instance = RequestContext(request))
  except Exception as e:
    l.info(request.user.username + ': Exception in viewing company feedback list.')
    l.exception(e)
    return handle_exc(e, request)

@login_required
@user_passes_test(lambda u: u.groups.filter(name__in=('Student', 'Placement Admin')).exists(), login_url=login_url)
def company(request, company_id) :
  """
  Display feedback of a particular company.
  """
  try :
    # TODO : Implement paging
    l.info(request.user.username + ': Viewing Feedback for ' + company_id)
    company = get_object_or_404(Company, id = company_id)
    year = company.year
    feedbacks = Feedback.objects.filter(company = company_id).order_by('-date')
    session = str(year) + '-' + str(int(year)+1)
    placed_companies = []
    for feedback in feedbacks :
      # Try to get the company name in which the student was placed.
      # Do not care if data not found.
      try :
        # A student may get placed in two companies
        placed_companies.append(','.join(Results.objects.filter(student = feedback.student).values_list('company__name', flat=True)))
      except Results.DoesNotExist :
        placed_companies.append(None)
    feedbacks = zip(feedbacks, placed_companies)
    return render_to_response('placement/company_feedback.html', {
        'session' : session,
        'feedbacks' : feedbacks,
        'company' : company,
        }, context_instance = RequestContext(request))
  except Exception as e:
    l.info(request.user.username + ': Exception in viewing company feedback for ' + company_id)
    l.exception(e)
    return handle_exc(e, request)

@login_required
@user_passes_test(lambda u: u.groups.filter(name='Student').exists(), login_url=login_url)
def fill(request) :
  """
  Take feedback about a company from the user.
  """
  try :
    l.info(request.user.username + ': Giving Feedback for a company')
    student = request.session['student']
    plac_person = request.session['plac_person']
    if plac_person.status != 'VRF' :
      l.info(request.user.username + ': Giving feedback for a company, but user not Verified')
      return TemplateView(request, template="404.html")
    if request.method == 'POST' :
      form = forms.Feedback(request.POST)
      if form.is_valid() :
        company = form.cleaned_data['company']
        # A student cannot fill feedback for a company multiple times?
        if Feedback.objects.filter(student = student, company = company).exists() :
          messages.error(request, 'You have already given feedback for "' + company.name + '"')
          return HttpResponseRedirect(reverse('placement.views_feedback.company', args=[str(company.id)]))
        feedback_text = ''
        for i in range(1,7) :
          if form.cleaned_data['feedback'+str(i)] :
            feedback_text = feedback_text + '<p class="feedback_question">' + PC.FEEDBACK_QUESTIONS[i-1] + '</p>'
            feedback_text = feedback_text + '<p class="feedback_answer">' + form.cleaned_data['feedback'+str(i)] + '</p>'
        feedback_text = feedback_text.replace('\n',' ').replace('\r','').replace('\t',' ')
        Feedback.objects.create(student = student, company = company, feedback = feedback_text)
        l.info(request.user.username + ': Successfully gave feedback for ' + str(company.id))
        messages.success(request, 'Your feedback for "' + company.name + '" was saved successfully.')
        return HttpResponseRedirect(reverse('placement.views_feedback.company', args=[str(company.id)]))
    else :
      form = forms.Feedback()
    # Set questions as labels in the form.
    for i in range(1,7) :
      form.fields['feedback'+str(i)].label=PC.FEEDBACK_QUESTIONS[i-1]
    return render_to_response('placement/feedback_add.html', {
        'form' : form,
        'action' : reverse('placement.views_feedback.fill')
        }, context_instance = RequestContext(request))
  except Exception as e:
    l.info(request.user.username + ': Exception in giving feedback.')
    l.exception(e)
    return handle_exc(e, request)

@login_required
@user_passes_test(lambda u: u.groups.filter(name__in=('Student', 'Placement Admin')).exists(), login_url=login_url)
def as_pdf(request, feedback_id) :
  """
  Return a pdf file containing a particular feedback.
  """
  try :
    l.info(request.user.username + ': Downloading feedback with id = ' + feedback_id)
    feedback = get_object_or_404(Feedback, id = feedback_id)
    session = str(feedback.company.year) + '-' + str(feedback.company.year+1)[2:4]
    placed_in = ','.join(Results.objects.filter(student = feedback.student).values_list('company__name', flat=True))
    # TODO : Use proper formatting
    html  = render_to_string('placement/feedback.html',
                             { 'pagesize' : 'A4',
                               'session' : session,
                               'feedback' : feedback,
                               'placed_in' : placed_in
                               },
                             context_instance = RequestContext(request))
    result = StringIO.StringIO()
    pdf = pisa.pisaDocument(StringIO.StringIO(html.encode('UTF-8')), result)
    if pdf.err :
      l.info(request.user.username + ': Error in downloading feedback as PDF')
      messages.error(request, 'An error occured while generating the PDF file.')
      return HttpResponseRedirect(reverse('placement.views.index'))
    response = HttpResponse(result.getvalue(), mimetype='application/pdf')
    filename = feedback.company.name + '_' + feedback.student.name + '_PlacementFeedback_' + session
    # sanitise filename
    filename = sanitise_for_download(filename)
    response['Content-Disposition'] = 'attachment; filename=' + filename + '.pdf'
    response['Content-Length'] = len(result.getvalue())
    return response
  except Exception as e:
    l.info(request.user.username + ': Exception in viewing feedback ' + feedback_id)
    l.exception(e)
    return handle_exc(e, request)
