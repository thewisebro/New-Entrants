from smtplib import SMTPException
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest, Http404
from django.shortcuts import render, get_object_or_404
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.template import RequestContext 
from django.db.models import Q
import json as simplejson
from django.db.models import Count
from django.core.mail import EmailMessage

from nucleus.models import Branch, User, Faculty
from facapp.models import *
from facapp.utils import handle_exc
from facapp.forms import BooksAuthoredForm, RefereedJournalPapersForm, PhotoUploadForm, ResumeUploadForm
from core.forms import BaseForm, BaseModelForm # , BaseModelFormFunction, ConfirmDeleteForm
from api import model_constants as MC

@login_required
@user_passes_test(lambda u: u.groups.filter(name='Faculty').count() != 0)  
def mass_mailer(request):
  try:
    faculty = request.user.faculty
    # If the form was submitted.
    if request.method == 'POST':
      enrollment_nos = request.POST.getlist('student')
      attachments = request.FILES.getlist('attachments')
      subject = request.POST['subject']
      mail_body = request.POST['mail_body']
      persons = []
      for enrollment_no in enrollment_nos:
        p = User.objects.all().filter(username=enrollment_no)
        if len(p):
          persons += p
      alternate_mail_ids = map(lambda x: x.email_id, persons)
      msg = EmailMessage(subject, mail_body, faculty.user.username + '@iitr.ernet.in', alternate_mail_ids)
      msg.content_subtype = 'html'
      for attachment in attachments:
        msg.attach(attachment.name, attachment.read())
      msg.send(fail_silently=False)
      # If above call returns, then all mails sent.
      messages.success(request, 'All mails were successfully sent.')
      return HttpResponseRedirect(reverse('facapp.views.index'))

    # Form was not submitted.
    branch_list = Branch.objects.filter(department=faculty.department)
    return render(request, 'facapp/mass_mailer.html', {
        'branch_list': branch_list,
        'action': '/facapp/mass_mailer/',
        })
  # send_mail might throw an SMTPException
  except SMTPException as se:
    return handle_exc(e, request, 'Error communicating with the mail server. Please try again later. The issue has beeen reported.')
  except Exception as e:
    return handle_exc(e, request)

# AJAX requests start here.
@login_required
@user_passes_test(lambda u: u.groups.filter(name='Faculty').count() != 0)  
def choose_semester(request):
  callback = request.GET.get('callback', '')
  try:
    faculty = request.user.faculty
    # If an AJAX request was made.
    if request.is_ajax():
      branch = request.POST['branch']
      ret = map(lambda x:{'count':x['d'], 'sem_code':x['semester'], 'sem_value':MC.get_value_from_key(MC.SEMESTER_CHOICES, x['semester'])}, Person.objects.filter(branch=branch).values('semester').annotate(d=Count('semester')))
      return HttpResponse(callback + '(' + simplejson.dumps(ret) + ')', mimetype='application/json')
    # If any other request is made then raise error.
    raise Exception('Invalid request.')
  except Exception as e:
    return HttpResponse(callback + '(' + simplejson.dumps([{'success': False}, {'msg': 'Unable to fetch semester details. The problem has been reported. Please try again later.'}]) + ')', mimetype='application/json') 

@login_required
@user_passes_test(lambda u: u.groups.filter(name='Faculty').count() != 0)  
def show_student_list(request):
  callback = request.GET.get('callback', '')
  try:
    faculty = request.user.faculty
    # If an AJAX request was made.
    if request.is_ajax():
      branch = request.POST['branch']
      semester = request.POST['semester']
      ret = map(lambda x:{'name':x[0], 'enrollment_no':User.objects.get(pk=x[1]).username}, Person.objects.filter(branch=branch).filter(semester=semester).values_list('name', 'user'))
      return HttpResponse(callback + '(' + simplejson.dumps(ret) + ')', mimetype='application/json')
    # If any other request is made then raise error.
    raise Exception('Invalid request.')
  except Exception as e:
    return HttpResponse(callback + '(' + simplejson.dumps([{'success': False}, {'msg': 'Unable to fetch student details. The problem has been reported. Please try again later.'}]) + ')', mimetype='application/json') 

# AJAX requests end here.
