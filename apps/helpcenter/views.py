import json as simplejson
import smtplib
import logging

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.contrib.auth.models import Group
from django.shortcuts import get_object_or_404, render
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.template.defaultfilters import urlize
from django.conf import settings
from django.utils.html import escape

from core import forms
from helpcenter.models import *
from api.utils import get_client_ip
from helpcenter.forms import *
from nucleus.models import User, WebmailAccount

logger = logging.getLogger('channel-i_logger')

@login_required
def pagelet_index(request):
  ResponseForm = ResponseFormGen(request.user)
  form = ResponseForm()
  user_in_img = 1 if request.user.in_group('IMG Member') else 0
  return render(request, 'helpcenter/pagelet_index.html', {
      'form': form,
      'user_in_img': user_in_img
  })

@login_required
def feedbacks(request):
  return HttpResponseRedirect(reverse('helpcenter.views.queries'))

def reply_dict(reply):
  username = reply.user.username
  if reply.by_img:
    username = 'img'
    user_photo = '/static/images/nucleus/img_dp.png'
  else:
    user_photo = response.user.photo_url
  return {
    'username' : username,
    'user_photo' : user_photo,
    'response_id' : reply.response.pk,
    'text' : urlize(escape(reply.text)).replace('\n','<br>'),
  }

def response_dict(response, user=None):
  replies = map(reply_dict, response.reply_set.all())
  res_dict = {
    'id' : response.pk,
    'username' : response.user.username if response.user else 'anonymous',
    'user_name' : response.user.html_name if response.user else 'Anonymous User',
    'user_photo' : response.user.photo_url,
    'app' : response.app,
    'text' : urlize(escape(response.text)).replace('\n','<br>'),
    'replies' : replies,
    'datetime' : response.datetime_created.strftime('%Y-%m-%d %H:%M:%S'),
    'response_type' : response.response_type,
  }
  if user and user.in_group('IMG Member'):
    res_dict.update({
        'resolved': response.resolved
    })
  return res_dict

@login_required
def fetch(request):
  if request.is_ajax() and request.method == 'GET':
    user_in_img = request.user.in_group('IMG Member')
    action = request.GET['action']
    pk = request.GET['id']
    number = int(request.GET['number'])
    responses = Response.objects.all() if user_in_img else Response.objects.filter(user=request.user)
    if action == 'next':
      responses = responses.filter(datetime_created__lt = Response.objects.get(pk=pk).datetime_created)
    if action == 'exact':
      responses = responses.filter(pk=pk)
      number = 1
    json = simplejson.dumps({
        'responses':map(lambda r:response_dict(r,request.user),responses[:number]),
        'more':int(responses.count()>number)
    })
    return HttpResponse(json,content_type='application/json')
  return HttpResponse("")

@login_required
def give_response(request):
  if request.is_ajax() and request.method == 'POST':
    text = request.POST['text']
    app = request.POST['app']
    response_type = request.POST['response_type']
    if text:
      logger.info("Helpcenter : User("+request.user.username+") gave a response ("+response_type+").")
      response = Response.objects.create(user=request.user,text=text,app=app,response_type=response_type)
      json = simplejson.dumps({'response':response_dict(response)})
      return HttpResponse(json,content_type='application/json')
  return HttpResponse("")

@login_required
def give_reply(request):
  if request.is_ajax() and request.method == 'POST':
    user_in_img = request.user.in_group('IMG Member')
    text = request.POST['text']
    response = Response.objects.get(pk=request.POST['response_id'])
    if text and (user_in_img or response.user == request.user):
      logger.info("Helpcenter : User("+request.user.username+") replied on a response (id="+str(response.pk)+").")
      reply = Reply.objects.create(user=request.user,response=response,text=text)
      if not response.user:
        send_a_mail(response.email, text)
      json = simplejson.dumps({'reply':reply_dict(reply)})
      return HttpResponse(json,content_type='application/json')
  return HttpResponse("")

def send_a_mail(email, msg):
  fromaddr = 'img@iitr.ac.in'
  toaddrs  = [email, 'img@iitr.ac.in']
  toaddrs_shown = email
  subject  = "Regarding Channel-i login problem"
  message = ("From: %s\r\nTo: %s\r\nSubject: %s\r\n\r\n%s" % (fromaddr, toaddrs_shown, subject, msg))
  server = smtplib.SMTP(settings.POP3_HOST)
  server.set_debuglevel(0)
  server.sendmail(fromaddr, toaddrs, message)
  server.quit()

@login_required
def set_resolved(request):
  if request.is_ajax() and request.method == 'POST' and request.user.in_group('IMG Member'):
    response = Response.objects.get(pk=request.POST['response_id'])
    value = int(request.POST['value'])
    response.resolved = True if value else False
    response.save()
    logger.info("Helpcenter : User("+request.user.username+") set resolved = '"+('True' if value else 'False')+"' in response (id="+str(response.pk)+").")
    json = simplejson.dumps({'response':response_dict(response,request.user)})
    return HttpResponse(json,content_type='application/json')
  return HttpResponse('')

def login_help(request, username=''):
  post = False
  form = LoginHelpForm(initial={'username':username})
  option = request.GET.get('option', None)
  close = False
  if request.method == 'POST':
    if option == 'ask_help':
      post = True
      form = LoginHelpForm(request.POST)
      if form.is_valid():
        user_type = form.cleaned_data['user_type']
        username = form.cleaned_data['username']
        enrollment_no = str(form.cleaned_data['enrollment_no'])
        email = form.cleaned_data['email']
        text = form.cleaned_data['text']
        response_text = "Having trouble Signing in to Channel I.\n"+\
               (" User Type: "+ user_type.capitalize())+'\n'+\
               (" Username: "+username+'\n' if username else '')+\
               ((" Enrollment No: "+enrollment_no+'\n' if enrollment_no else '') if user_type == 'student' else '')+\
               (" Email Id: "+email)+'\n'+\
               (" Problem: "+text)
        ip = get_client_ip(request)
        if ip:
          logger.info("Helpcenter : Anonymous user asked for login help from IP Address ("+ip+").")
        Response.objects.create(email = email,text = response_text,app='Channel I Login',response_type='help')
        messages.info(request,'Thank You. We will look into your problem and reply you soon.')
        close = True
    else:
      close = True
  return render(request, 'helpcenter/login_help.html', {
      'form': form,
      'post': post,
      'option': option,
      'close': close
  })


@login_required
def feedback(request):
  ResponseForm = ResponseFormGen(request.user)
  form = ResponseForm()
  close = False
  if request.method == 'POST':
    form = ResponseForm(request.POST)
    if form.is_valid():
      text = form.cleaned_data['text']
      app = form.cleaned_data['app']
      Response.objects.create(user=request.user,text=text,response_type='feedback',app=app)
      messages.info(request,'Thank you for your feedback.')
      logger.info("Helpcenter : User("+request.user.username+") gave a feedback.")
      close = True
  return render(request, 'helpcenter/feedback.html', {
      'form':form,
      'close':close
  })
