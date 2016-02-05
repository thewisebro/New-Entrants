from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from new_entrants.serializer import *
from rest_framework.generics import ListAPIView, RetrieveAPIView
from django.core.validators import validate_email
from django.views.generic import TemplateView
import json as simplejson
from django.conf import settings
from django.contrib import messages

from new_entrants.models import *
from api import model_constants as MC

def get_domain():
  if settings.SITE=='INTRANET':
    return 'https://channeli.in/'
  else:
    return 'http://people.iitr.ernet.in/'

@login_required
def create_user(request):
  data = request.POST
  user = request.user
  email = data.get('email','')
  try:
    validate_email(email)
  except:
    return HttpResponse(simplejson.dumps({'error':'email'}), content_type='application/json')
  fb_link = data.get('fb_link','')
  if fb_link == '':
    return HttpResponse(simplejson.dumps({'error':'fb_link'}), content_type='application/json')
  state = data.get('state','')
  if state == '' or state not in dict(MC.STATE_CHOICES):
    return HttpResponse(simplejson.dumps({'error':'state'}), content_type='application/json')
  hometown = data.get('hometown','')
  phone_no = data.get('phone_no','').trim()
  if phone_no == '':
    return HttpResponse(simplejson.dumps({'error':'phone_no'}), content_type='application/json')
  phone_privacy = data.get('phone_privacy','')
  profile_privacy = data.get('profile_privacy','')
  if user.groups.filter(name='New Entrant').exists():
    junior = Student_profile()
    junior.user=user
    junior.email=email
    junior.fb_link=fb_link
    junior.state=state
    junior.hometown=hometown
    junior.phone_no=phone_no
    junior.phone_privacy = (phone_privacy == 'True')
    junior.profile_privacy = (profile_privacy == 'True')
    junior.save()
  else :
    senior = Senior_profile()
    senior.user=user
    senior.email=email
    senior.fb_link=fb_link
    senior.state=state
    senior.hometown=hometown
    senior.phone_no=phone_no
    senior.save()
  data = {'status':'success'}
  data['category'] = 'peer' if user.groups.filter(name='New Entrant').exists() else 'senior'
  return HttpResponse(simplejson.dumps(data), content_type='application/json')

def blogs(request):
  def blog_dict(blog):
    return {
      'title':blog.title,
      'group':blog.group.name,
      'dp_link':get_domain() + 'photo/' + str(blog.group.user.username),
      'description':blog.description,
      'date':blog.date_published.strftime('%Y-%m-%d %H:%M:%S'),
      'blog_url':get_domain() + 'new_entrants/' + str(blog.group.user.username) + '/' + blog.slug
    }

  query_set = Blog.objects.all().order_by('-date_published')
  data = simplejson.dumps(map(blog_dict,query_set))
  return HttpResponse(data, content_type='application/json')

def blogs_group(request, group_id=None):
  def blog_dict(blog):
    return {
      'title':blog.title,
      'group':blog.group.name,
      'dp_link':get_domain() + 'photo/' + str(blog.group.user.username),
      'description':blog.description,
      'date':blog.date_published.strftime('%Y-%m-%d %H:%M:%S'),
      'blog_url':get_domain() + 'new_entrants/' + str(blog.group.user.username) + '/' + blog.slug
    }

  try:
    group = Group.objects.get(user__username=group_id)
    query_set = Blog.objects.filter(group=group).order_by('-date_published')
    data = simplejson.dumps(map(blog_dict,query_set))
    return HttpResponse(data, content_type='application/json')
  except:
    return HttpResponseRedirect('/new_entrants/blogs')

def blogs_view(request, group_id=None, slug=None):
  def blog_dict(blog):
    return {
      'title':blog.title,
      'group':blog.group.name,
      'dp_link':get_domain() + 'photo/' + str(blog.group.user.username),
      'description':blog.description,
      'date':blog.date_published.strftime('%Y-%m-%d %H:%M:%S'),
      'content':blog.content
    }

  try:
    group = Group.objects.get(user__username=group_id)
    try:
      query_set = Blog.objects.get(group=group,slug=slug)
      data = simplejson.dumps(blog_dict(query_set))
      return HttpResponse(data, content_type='application/json')
    except:
      return HttpResponseRedirect('/new_entrants/blogs/'+group_id)
  except:
    return HttpResponseRedirect('/new_entrants/blogs/')

def request_connect(request):       #untested
  data = {'status':'fail'}
  try:
    accept_id = request.GET.get('to','')
    sender = request.user
    if not sender.groups.filter(name='New Entrant').exists():
      raise Exception('Request sent by senior')
    acceptor = User.objects.get(user__username=accept_id)
    if Request.objects.filter(sender=sender,acceptor=acceptor).exists()
      raise Exception('Request already exists')
    r = Request()
    r.sender = sender
    r.acceptor = acceptor
    r.category = 'peer' if acceptor.groups.filter(name='New Entrant').exists() else 'senior'
    r.save()
    data['status'] = 'success'
  except:
    pass
  data = simplejson.dumps(data)
  return HttpResponse(data, content_type='application/json')

def accept_connect(request):        #untested
  data = {'status':'fail'}
  try:
    accept_id = request.GET.get('from','')
    acceptor = request.user
    sender = User.objects.get(user__username=accept_id)
    category = 'peer' if acceptor.groups.filter(name='New Entrant').exists() else 'senior'
    r = Request.objects.get(sender=sender,acceptor=acceptor,category=category)
    r.is_accepted=True
    r.save()
    data['status'] = 'success'
  except:
    pass
  data = simplejson.dumps(data)
  return HttpResponse(data, content_type='application/json')

@login_required
def pending_requests(request):      #untested
  def user_dict(req):
    return {  #check for branch
      'user':req.sender.username,
      'name':req.sender.name,
      'state':req.sender.state,
      'hometown':req.sender.hometown,
    }

  user = request.user
  data = {'status':'fail'}
  try:
    category = 'peer' if user.groups.filter(name='New Entrant').exists() else 'senior'
    query_set = Request.objects.filter(acceptor=user,category=category,is_accepted=False)
    data = simplejson.dumps(map(user_dict,query_set))
  except:
    data = simplejson.dumps(data)
    pass
  return HttpResponse(data, content_type='application/json')

@login_required
def accepted(request):        #untested #complete
  def senior_dict(req):
    return {
      'name':req.senior_profile.user.name,
      'state':req.senior_profile.state,
      'hometown':req.senior_profile.hometown,
      'branch_code':req.senior_profile.branch.code,
      'branch':req.senior_profile.branch.name,
      'fb_link':req.senior_profile.fb_link,
      'email':req.senior_profile.email,
      'contact':req.senior_profile.phone_no
    }

  def student_dict(req):
    return {
      'name':req.student_profile.user.name,
      'state':req.student_profile.state,
      'hometown':req.student_profile.hometown,
      'branch_code':req.student_profile.branch.code,
      'branch':req.student_profile.branch.name,
      'fb_link':req.student_profile.fb_link,
      'email':req.student_profile.email,
      'contact':req.student_profile.phone_no
    }


  user = request.user
  data = {'status':'fail'}
  try:
    sort_by = request.POST.get('sort_by','')
    category = request.POST.get('category','')
    if sort_by == 'branch':
      query_set = Request.objects.filter(sender=user,category=category,is_accepted=True).order_by(acceptor__user__branch)
    else if sort_by == 'location':
      query_set =  Request.objects.filter(sender=user,category=category,is_accepted=True).order_by(acceptor__hometown)
    else:
      query_set = Request.objects.filter(sender=user,category=category,is_accepted=True)
    if category = 'peer':
      query_users = [lambda user: Student_profile.objects.get(user=user) for user in query_set]
      data = simplejson.dumps(map(student_dict,query_users))
    else:
      query_users = [lambda user: Senior_profile.objects.get(user=user) for user in query_set]
      data = simplejson.dumps(map(senior_dict,query_users))
  except:
    data = simplejson.dumps(data)
    pass
  return HttpResponse(data, content_type='application/json')
