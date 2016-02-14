from django.contrib.auth.models import Group as GG
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
from new_entrants.forms import *
from nucleus.models import Branch, User
from api import model_constants as MC

def get_domain():
  if settings.SITE=='INTRANET':
    return 'https://channeli.in/'
  else:
    return 'http://people.iitr.ernet.in/'

def get_junior_contact(junior):
  if junior.phone_privacy == True:
    return ''
  else:
    return junior.phone_no

def get_junior_branch(junior):
  if junior.is_branch == True:
    return {'code':junior.user.student.branch.code,'name':junior.user.student.branch.name}
  else :
    return {'code':'','name':''}

def userinfo(request):
  data = {'status':'fail'}
  if request.user.is_authenticated():
    user = request.user
    if user.groups.filter(name='New Entrant').exists():
      data['name'] = user.name
      data['category'] = 'junior'
      junior = Student_profile.objects.get(user=user)
      data['branch'] = get_junior_branch(junior)
      data['email'] = junior.email
      data['fb_link'] = junior.fb_link
      data['phone'] = junior.phone_no
      data['state'] = junior.get_state_display()
      data['hometown'] = junior.hometown
      data['phone_privacy'] = junior.phone_privacy
      data['profile_privacy'] = junior.profile_privacy
      data['status'] = 'success'
    else:
      data['name'] = user.name
      data['category'] = 'senior'
      senior = Senior_profile.objects.get(user=user)
      data['branch'] = {'code':senior.user.student.branch.code,'name':senior.user.student.branch.name}
      data['year'] = (senior.user.student.semester_no+1)/2
      data['email'] = senior.email
      data['fb_link'] = senior.fb_link
      data['phone'] = senior.phone_no
      data['state'] = senior.get_state_display()
      data['hometown'] = senior.hometown
      data['enrollment_no'] = user.username
      data['status'] = 'success'
  return HttpResponse(simplejson.dumps(data), content_type='application/json')

def register(request):      #for new entrants   #coded    #tested browser
  if not request.user.is_authenticated():
    if request.method == 'POST':
      print request.POST
      data = {'status':'fail'}
      form = RegisterForm(request.POST)
      if form.is_valid():
        rec = form.cleaned_data
        username = rec['username']
        if not User.objects.filter(username=username).exists():
          password = rec['password1']
          name = rec['name']
          email = rec['email']
          user = User.objects.create_user(username=username,password=password,email=email,name=name)
          group = GG.objects.get(name='Student')
          group.user_set.add(user)
          group = GG.objects.get(name='New Entrant')
          group.user_set.add(user)
          fb_link = rec['fb_link']
          phone = rec['phone_no']
          state = rec['state']
          branch = rec['branch']
          hometown = rec['hometown']
          profile_privacy = rec['profile_privacy']
          phone_privacy = rec['phone_privacy']
          junior = Student_profile()
          try:
            branch = Branch.objects.get(code=branch)
            student = Student()
            student.user = user
            student.branch = branch
            student.semester = 'UG10'
            student.semester_no = 1
            student.admission_year = 2016
            student.admission_semtype = 'A'
            student.save()
            junior.is_branch = True
          except:
            junior.is_branch = False
            pass
          junior.user=user
          junior.email=email
          junior.fb_link=fb_link
          junior.state=state
          junior.hometown=hometown
          junior.phone_no=phone
          junior.phone_privacy = phone_privacy
          junior.profile_privacy = profile_privacy
          junior.save()
          data['status'] = 'success'
        else:
          data['error'] = 'Username already exists.'
      return HttpResponse(simplejson.dumps(data), content_type='application/json')
    else:
      form = RegisterForm()
      return render(request, 'new_entrants/register.html', {'form': form.as_p() })
  else:
    return HttpResponseRedirect('/new_entrants/')

def update(request):    #coded
  if request.method == 'POST':
    data = request.POST
    user = request.user
    email = data.get('email','')
    try:
      validate_email(email)
    except:
      return HttpResponse(simplejson.dumps({'error':'email'}), content_type='application/json')
    state = data.get('state','')
    if state not in dict(MC.STATE_CHOICES):
      return HttpResponse(simplejson.dumps({'error':'state'}), content_type='application/json')
    fb_link = data.get('fb_link','')
    hometown = data.get('hometown','')
    phone_no = data.get('phone_no','')
    phone_privacy = data.get('phone_privacy','')
    profile_privacy = data.get('profile_privacy','')
    if user.groups.filter(name='New Entrant').exists():
      phone_privacy = data.get('phone_privacy','')
      profile_privacy = data.get('profile_privacy','')
      junior = Student_profile()
      try:
        branch_name = data.get('branch','')
        branch = Branch.objects.get(name=branch_name)
        student = Student()
        student.user = user
        student.branch = branch
        student.semester = 'UG10'
        student.semester_no = 1
        student.admission_year = 2016
        student.admission_semtype = 'A'
        student.save()
        junior.is_branch = True
      except:
        pass
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
    data['category'] = 'junior' if user.groups.filter(name='New Entrant').exists() else 'senior'
    return HttpResponse(simplejson.dumps(data), content_type='application/json')
  else:
    return HttpResponse(simplejson.dumps({'error':''}), content_type='application/json')

def blogs(request):     #coded
  def blog_dict(blog):
    return {
      'title':blog.title,
      'group':blog.group.name,
      'dp_link':get_domain() + 'photo/' + str(blog.group.user.username),
      'description':blog.description,
      'date':blog.date_published.strftime('%Y-%m-%d %H:%M:%S'),
      'blog_url':get_domain() + 'new_entrants/' + str(blog.group.user.username) + '/' + blog.slug,
      'id':blog.pk
    }

  query_set = Blog.objects.all().order_by('-date_published')
  action = request.GET.get('action','')
  if action == 'next':
    query_set = query_set.filter(pk__gt = request.GET['id'])
  data = simplejson.dumps({'blogs':map(blog_dict,query_set[:10]),'more':int(query_set.count()>10)})
  return HttpResponse(data, content_type='application/json')

def blogs_group(request, group_id=None):      #coded
  def blog_dict(blog):
    return {
      'title':blog.title,
      'group':blog.group.name,
      'dp_link':get_domain() + 'photo/' + str(blog.group.user.username),
      'description':blog.description,
      'date':blog.date_published.strftime('%Y-%m-%d %H:%M:%S'),
      'blog_url':get_domain() + 'new_entrants/' + str(blog.group.user.username) + '/' + blog.slug,
      'id':blog.pk
    }

  try:
    group = Group.objects.get(user__username=group_id)
    query_set = Blog.objects.filter(group=group).order_by('-date_published')
    action = request.GET.get('action','')
    if action == 'next':
      query_set = query_set.filter(pk__gt = request.GET['id'])
    data = simplejson.dumps({'blogs':map(blog_dict,query_set[:10]),'more':int(query_set.count()>10)})
    return HttpResponse(data, content_type='application/json')
  except Exception as e:
    print str(e)
    return blogs(request)

def blogs_view(request, group_id=None, slug=None):      #coded
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
      return blogs_group(request,group_id)
  except:
    return blogs(request)

@login_required
def request_connect(request):       #coded
  data = {'status':'fail'}
  if request.method == 'POST':
    try:
      user = request.user
      if not user.groups.filter(name='New Entrant').exists():
        raise Exception('Request sent by senior')
      junior = Student_profile.objects.get(user=user)
      senior_id = request.POST.get('to','')
      senior = Senior_profile.objects.get(user__username=senior_id)
      if Request.objects.filter(senior=senior,junior=junior).exists():
        raise Exception('Request already exists')
      r = Request()
      r.senior = senior
      r.junior = junior
      r.save()
      data['status'] = 'success'
    except:
      pass
  data = simplejson.dumps(data)
  return HttpResponse(data, content_type='application/json')

@login_required
def accept_connect(request):        #coded
  data = {'status':'fail'}
  if request.method == 'POST':
    try:
      user = request.user
      if user.groups.filter(name='New Entrant').exists():
        raise Exception('Request sent by junior')
      senior = Senior_profile.objects.get(user=user)
      junior_id = request.POST.get('from','')
      junior = Student_profile.objects.get(user__username=junior_id)
      r = Request.objects.get(senior=senior,junior=junior)
      r.is_accepted = True
      r.save()
      data['status'] = 'success'
    except:
      pass
  data = simplejson.dumps(data)
  return HttpResponse(data, content_type='application/json')

@login_required
def pending_requests(request):
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
def accepted(request):      #coded
  def senior_dict(senior):
    return {
      'name':senior.user.name,
      'state':senior.state,
      'hometown':senior.hometown,
      'branch_code':senior.user.student.branch.code,    #check if code required or name
      'branch':senior.user.student.branch.name,
      'fb_link':senior.fb_link,
      'email':senior.email,
      'contact':senior.phone_no
    }

  def student_dict(junior):
    return {
      'name':junior.user.name,
      'state':junior.state,
      'hometown':junior.hometown,
      'branch':get_junior_branch(junior),   #check if code required or name
      'fb_link':junior.fb_link,
      'email':req.student_profile.email,
      'contact':get_junior_contact(junior)
    }


  user = request.user
  data = {'status':'fail'}
  if request.method == 'POST':
    try:
      sort_by = request.POST.get('sort_by','')   #options are 'location' and 'branch'
      if user.groups.filter(name='New Entrant').exists():
        junior = Student_profile.objects.get(user=user)
        if junior.is_branch and sort_by == 'branch':
          branch = junior.user.student.branch
          query_set = Request.objects.filter(junior=junior,is_accepted=True,senior__user__student__branch=branch)
        elif sort_by == 'location':
          state = junior.state
          query_set = Request.objects.filter(junior=junior,is_accepted=True,senior__state=state)
        else:
          query_set = Request.objects.filter(junior=junior,is_accepted=True)
        data = simplejson.dumps(map(senior_dict,query_set))
      else:
        senior = Senior_profile.objects.get(user=user)
        query_set = Request.objects.filter(senior=senior,is_accepted=True)
        data = simplejson.dumps(map(student_dict,query_users))
    except:
      data = simplejson.dumps(data)
      pass
  return HttpResponse(data, content_type='application/json')
