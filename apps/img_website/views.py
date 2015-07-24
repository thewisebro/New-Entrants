from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.template.loader import render_to_string
from django.template import Context
from django.conf import settings
from django.forms.models import modelformset_factory
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.encoding import smart_str
#from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.core.mail import send_mail
from django.core import serializers

from img_website.models import *
from nucleus.models import Student, User
from filemanager import FileManager

import os
import subprocess
import datetime
import smtplib
import json

def user_team_member(user):
  ''' returns true if a user is a team member '''
  student = get_object_or_404(Student, pk = user.pk)
  if not TeamMember.objects.filter(member_name = student).exists():
    return False
  return True

def index(request):
  ''' Home '''
  works=RecentWorks.objects.filter(state='Published').order_by('-date')[:3]
  posts=BlogPost.objects.filter(state='Published').order_by('-date')
  return render(request, 'img_website/index.html', {'work_list':works,'post_list':posts,})

def about(request):
  ''' About '''
  count_members = User.objects.filter(groups__name = 'IMG Member', student__passout_year__isnull = True).count()
  return render(request, 'img_website/about.html', {'count':count_members})

def contact(request):
  ''' Contact '''
  if request.method == 'POST':
    contact_form = ContactForm(request.POST)
    if contact_form.is_valid():
      sender_name = contact_form.cleaned_data['name']
      sender_mail = contact_form.cleaned_data['email']
      message = contact_form.cleaned_data['message']
      mail_server = smtplib.SMTP(settings.EMAIL_HOST)
      messages.add_message(request, messages.SUCCESS, 'Your message has been sent.')
      headers = "To:namit.ohri@gmail.com" + "\r\nFrom:" + sender_mail + "\r\n" +\
              "Subject: IMG messages\r\n"
      msg = headers + message + "\r\nFrom:" + sender_name
      mail_server.sendmail(sender_mail, ["img.iitr.img+img_website@gmail.com"], msg)
      mail_server.quit()
      return render(request, 'img_website/contact.html', {'contact_form':contact_form, })
  else:
    contact_form = ContactForm()
  return render(request, 'img_website/contact.html', {'contact_form':contact_form})

def post_list(request):
  ''' list of posts view for all users '''
  posts=BlogPost.objects.filter(state='Published').order_by('-date')
  paginator = Paginator(posts, 10)
  page = request.GET.get('page', '1')
  try:
    post_list_paged = paginator.page(page)
  except PageNotAnInteger:
    post_list_paged = paginator.page(1)
  except EmptyPage:
    post_list_paged = paginator.page(paginator.num_pages)

  return render(request, 'img_website/static_blog.html', {'post_list':posts,'post_list_paged':post_list_paged},)

@login_required()
@user_passes_test(lambda u: u.groups.filter(name='IMG Member').count() != 0)
def post_list_dynamic(request):
  ''' list of posts view for IMG Members and Alumni '''
  posts = BlogPost.objects.all().order_by('-date')
  paginator = Paginator(posts, 10)
  page = request.GET.get('page', '1')
  try:
    post_list_paged = paginator.page(page)
  except PageNotAnInteger:
    post_list_paged = paginator.page(1)
  except EmptyPage:
    post_list_paged = paginator.page(paginator.num_pages)

  return render(request, 'img_website/blog.html', {'post_list':posts,'post_list_paged':post_list_paged},)

@login_required()
@user_passes_test(lambda u: u.groups.filter(name='IMG Member').count() != 0)
def edit(request):
  user = request.user
  student = get_object_or_404(Student, pk = user.pk)
  deployed = False
  if request.method == 'POST' and request.POST.has_key('deploy') and settings.PRODUCTION:
    p = subprocess.Popen('deploy_img_website')
    p.communicate()
    deployed = True
  return render(request, 'img_website/edit.html', {'student':student, 'deployed':deployed})

def post_detail(request, slug):
  ''' view for a single post for all users '''
  post = get_object_or_404(BlogPost, slug = slug, state='Published')
  posts = BlogPost.objects.filter(state='Published').order_by('-date')
  user = post.author
  student = get_object_or_404(Student, pk = user.pk)
  author = get_object_or_404(TeamMember, member_name = student)
  index=0
  for current_post in posts:
    if current_post.slug == slug:
      break
    else:
      index += 1
  if index == posts.count()-1:
    post_prev = ''
  else:
    post_prev = posts[index+1]

  if index == 0:
    post_next = ''
  else:
    post_next = posts[index-1]

  return render(request, 'img_website/static_blog_post.html', {'post':post, 'post_list':posts, 'post_prev':post_prev, 'post_next':post_next, 'author':author},)

@login_required()
@user_passes_test(lambda u: u.groups.filter(name='IMG Member').count() != 0)
def post_detail_dynamic(request, slug):
  ''' view for a single post for IMG Members and Alumni '''
  post = get_object_or_404(BlogPost, slug = slug)
  user = post.author
  student = get_object_or_404(Student, pk = user.pk)
  author = get_object_or_404(TeamMember, member_name = student)
  posts = BlogPost.objects.all().order_by('-date')
  index=0
  for current_post in posts:
    if current_post.slug == slug:
      break
    else:
      index += 1
  if index == posts.count()-1:
    post_prev = ''
  else:
    post_prev = posts[index+1]

  if index == 0:
    post_next = ''
  else:
    post_next = posts[index-1]

  return render(request, 'img_website/blog_post.html', {'post':post, 'post_list':posts, 'post_prev':post_prev, 'post_next':post_next, 'author':author},)

@login_required()
@user_passes_test(lambda u: u.groups.filter(name='IMG Member').count() != 0)
def create_post(request):
  ''' view to create a blog post '''
  user = request.user
  if not user_team_member(user):
    return HttpResponse("You are not a team member yet.Add yourself to the team")
  if request.method == 'POST':
    new_post = PostCreateForm(request.POST, request.FILES)
    if new_post.is_valid():
      p=new_post.save(commit = False)
      p.author = get_object_or_404(User, username = user.username)
      p.save()
      return redirect(settings.IMG_WEBSITE_BASE_URL+'/dynamic_blog/')
  else:
    new_post = PostCreateForm()
  return render(request, 'img_website/create.html', {"form":new_post,})

@login_required()
@user_passes_test(lambda u: u.groups.filter(name='IMG Member').count() != 0)
def update_post(request, slug):
  ''' view to update a previously written blog post '''
  post = get_object_or_404(BlogPost, slug = slug)
  form = PostUpdateForm(instance = post)
  if request.method == 'POST':
    form = PostUpdateForm(request.POST, instance = post)
    if form.is_valid():
      form.save()
      return redirect(settings.IMG_WEBSITE_BASE_URL+'/dynamic_blog/')
  else:
    return render(request, 'img_website/update.html', {"form":form,})

@login_required()
@user_passes_test(lambda u: u.groups.filter(name='IMG Member').count() != 0)
def delete_post(request, slug):
  ''' view to delete a blog post '''
  post = get_object_or_404(BlogPost, slug = slug)
  post.delete()
  return redirect(settings.IMG_WEBSITE_BASE_URL + '/dynamic_blog/')

def search_post(request):
  ''' view to search for a blog post '''
  posts_search = BlogPost.objects.filter(title__icontains=request.GET['post'], state='Published').order_by('-date')
  posts=BlogPost.objects.filter(state='Published').order_by('-date')
  paginator = Paginator(posts_search, 4)
  page = request.GET.get('page', '1')
  try:
    post_list_paged = paginator.page(page)
  except PageNotAnInteger:
    post_list_paged = paginator.page(1)
  except EmptyPage:
    post_list_paged = paginator.page(paginator.num_pages)

  return render(request, 'img_website/static_blog.html', {'post_list':posts,'post_list_paged':post_list_paged},)

def member_list(request):
  ''' Team page '''
  members = TeamMember.objects.filter(member_name__passout_year__isnull=True).order_by("member_name__user__name")
  return render(request, 'img_website/team2.html', {"members":members,})

@login_required()
@user_passes_test(lambda u: u.groups.filter(name='IMG Member').count() != 0)
def add_member(request):
  ''' View to add a student to img members '''
  user = request.user
  student = get_object_or_404(Student, pk = user.pk)
  Linkset = modelformset_factory(MemberLinks, exclude =('teammember',),extra = 3, max_num = 4)
  if TeamMember.objects.filter(member_name = student).exists():
    member = get_object_or_404(TeamMember, member_name = student)
    form = AddPicForm(instance = member)
    linkset = Linkset(queryset = MemberLinks.objects.filter(teammember = get_object_or_404(TeamMember, member_name = student)))
  else:
    form = AddMemberForm()
  if request.method == 'POST':
    if TeamMember.objects.filter(member_name = student).exists():
      form = AddPicForm(request.POST,request.FILES,instance = member)
      if form.is_valid():
        member_form = form.save(commit = False)
        member_form.member_name = student
        member_form.save()
      linkset = Linkset(request.POST)
      if linkset.is_valid():
        links = linkset.save(commit = False)
        for link in links:
          link.teammember = get_object_or_404(TeamMember, member_name = get_object_or_404(Student, pk = user.pk))
          link.save()
        return redirect(settings.IMG_WEBSITE_BASE_URL+'/team/')
    else:
      form = AddMemberForm(request.POST, request.FILES)
      if form.is_valid():
        member_form = form.save(commit = False)
        member_form.member_name = student
        member_form.save()
      member = get_object_or_404(TeamMember, member_name = student)
      pic_form = AddPicForm(instance = member)
      linkset = Linkset(queryset = MemberLinks.objects.filter(teammember = get_object_or_404(TeamMember, member_name = student)))
      return render(request, 'img_website/add_member.html', {"form":pic_form,"linkset":linkset})
  else:
    new_member = form
  if TeamMember.objects.filter(member_name = student).exists():
    return render(request, 'img_website/add_member.html', {"form":form,"linkset":linkset})
  else:
    return render(request, 'img_website/add_member.html', {"form":new_member})

def work_list(request, page='1'):
  ''' list of works view for all users '''
  works=RecentWorks.objects.filter(state='Published').order_by('-date')
  paginator = Paginator(works, 5)
#page = request.GET.get('page', '1')
  try:
    work_list_paged = paginator.page(page)
  except PageNotAnInteger:
    work_list_paged = paginator.page(1)
  except EmptyPage:
    work_list_paged = paginator.page(paginator.num_pages)

  return render(request, 'img_website/static_works.html', {'work_list':works,'work_list_paged':work_list_paged,})

@login_required()
@user_passes_test(lambda u: u.groups.filter(name='IMG Member').count() != 0)
def work_list_dynamic(request):
  ''' list of works view for IMG Members and Alumni '''
  works = RecentWorks.objects.all().order_by('-date')
  paginator = Paginator(works, 5)
  page = request.GET.get('page', '1')
  try:
    work_list_paged = paginator.page(page)
  except PageNotAnInteger:
    work_list_paged = paginator.page(1)
  except EmptyPage:
    work_list_paged = paginator.page(paginator.num_pages)

  return render(request, 'img_website/works.html', {'work_list':works,'work_list_paged':work_list_paged,})

def work_detail(request, slug):
  ''' detailed view for a particular work for all users '''
  work = get_object_or_404(RecentWorks, slug = slug,state='Published')
  works = RecentWorks.objects.filter(state='Published').order_by('-date')
  user = work.author
  student = get_object_or_404(Student, pk = user.pk)
  author = get_object_or_404(TeamMember, member_name = student)
  index=0
  for current_work in works:
    if current_work.slug == slug:
      break
    else:
      index += 1
  if index == works.count()-1:
    work_prev = ''
  else:
    work_prev = works[index+1]

  if index == 0:
    work_next = ''
  else:
    work_next = works[index-1]

  return render(request, 'img_website/static_work_post.html', {'work':work, 'work_list':works, 'work_prev':work_prev, 'work_next':work_next, 'author':author},)

@login_required()
@user_passes_test(lambda u: u.groups.filter(name='IMG Member').count() != 0)
def work_detail_dynamic(request, slug):
  ''' detailed view for a particular work for IMG Members and Alumni '''
  work = get_object_or_404(RecentWorks, slug = slug)
  works = RecentWorks.objects.all().order_by('-date')
  user = work.author
  student = get_object_or_404(Student, pk = user.pk)
  author = get_object_or_404(TeamMember, member_name = student)
  index=0
  for current_work in works:
    if current_work.slug == slug:
      break
    else:
      index += 1
  if index == works.count()-1:
    work_prev = ''
  else:
    work_prev = works[index+1]

  if index == 0:
    work_next = ''
  else:
    work_next = works[index-1]

  return render(request, 'img_website/work_post.html', {'work':work, 'work_list':works, 'work_prev':work_prev, 'work_next':work_next, 'author':author},)

@login_required()
@user_passes_test(lambda u: u.groups.filter(name='IMG Member').count() != 0)
def create_work(request):
  ''' View to add a new work post '''
  user = request.user
  if not user_team_member(user):
    return HttpResponse("You are not a team member yet.Add yourself to the team")
  if request.method == 'POST':
    new_work = WorkCreateForm(request.POST, request.FILES)
    if new_work.is_valid():
      w=new_work.save(commit = False)
      w.author = get_object_or_404(User, username = user.username)
      w.save()
      return redirect(settings.IMG_WEBSITE_BASE_URL+'/dynamic_works/')
  else:
    new_work = WorkCreateForm()
  return render(request, 'img_website/create.html', {"form":new_work,})

@login_required()
@user_passes_test(lambda u: u.groups.filter(name='IMG Member').count() != 0)
def update_work(request, slug):
  ''' View to update a previously written work post '''
  work = get_object_or_404(RecentWorks, slug = slug)
  form = WorkUpdateForm(instance = work)
  if request.method == 'POST':
    form = WorkUpdateForm(request.POST, request.FILES, instance = work)
    if form.is_valid():
      form.save()
      return redirect(settings.IMG_WEBSITE_BASE_URL+'/dynamic_works/')
  else:
    return render(request, 'img_website/update.html', {"form":form,})

@login_required()
@user_passes_test(lambda u: u.groups.filter(name='IMG Member').count() != 0)
def delete_work(request, slug):
  ''' view to delete a work post '''
  work = get_object_or_404(RecentWorks, slug = slug)
  work.delete()
  return redirect(settings.IMG_WEBSITE_BASE_URL + '/dynamic_works/')

@login_required()
@user_passes_test(lambda u: u.groups.filter(name='IMG Member').count() != 0)
def delete_post(request, slug):
  ''' view to delete a blog post '''
  post = get_object_or_404(BlogPost, slug = slug)
  post.delete()
  return redirect(settings.IMG_WEBSITE_BASE_URL + '/dynamic_blog/')

def status_post_list(request):
  status_posts=StatusPost.objects.filter(state='Published').order_by('-date')
  if settings.PRODUCTION:
    status_ajax_url = 'http://web.channeli.in/img_website/status_ajax/'
  else:
    status_ajax_url = '/img_website/status_ajax/'
  return render(request, 'img_website/status_post_list.html', {
      'status_post_list':status_posts,
      'status_ajax_url': status_ajax_url,
  })

@login_required()
def status_post_list_dynamic(request):
  user = request.user
  if user.in_group('IMG Member') is False:
    return render(request, 'img_website/restricted.html')
  status_posts = StatusPost.objects.all().order_by('-date')
  return render(request, 'img_website/status.html', {'status_post_list':status_posts,})

def status_dict(status_post):
  return {
    'pk': status_post.pk,
    'app': status_post.app,
    'content': status_post.content,
    'date': datetime.datetime.strftime(status_post.date, "%B %d, %Y"),
  }

def status_ajax(request):
  status_posts = StatusPost.objects.filter(state='Published').order_by('-date')
  data = json.dumps(map(status_dict, status_posts))
  response = HttpResponse(data, content_type='application/json')
  response['Access-Control-Allow-Origin'] = '*'
  return response

def status_post_detail(request, pk):
  status_post = StatusPost.objects.get(pk = pk,state='Published')
#works = RecentWorks.objects.filter(state='Published').order_by('-date')
#user = work.author
#student = Student.objects.get(pk = user.pk)
#author = TeamMember.objects.get(member_name = student)

  return render(request, 'img_website/work_post.html', {'work':status_post, })

@login_required()
def status_post_detail_dynamic(request, pk):
  user_logged = request.user
  if user_logged.in_group('IMG Member') is False:
    return render(request, 'img_website/restricted.html')
  status_post = StatusPost.objects.get(pk = pk)
#works = RecentWorks.objects.all().order_by('-date')
#user = work.author
#student = Student.objects.get(pk = user.pk)
#author = TeamMember.objects.get(member_name = student)

  return render(request, 'img_website/work_post.html', {'work':status_post, })

@login_required()
def create_status_post(request):
  user = request.user
  if user.in_group('IMG Member') is False:
    return render(request, 'img_website/restricted.html')
  if request.method == 'POST':
    new_post = StatusPostCreateForm(request.POST, request.FILES)
    if new_post.is_valid():
      p=new_post.save(commit = False)
      p.author = User.objects.get(username = user.username)
      p.save()
      return redirect(settings.IMG_WEBSITE_BASE_URL+'/dynamic_status/')
  else:
    new_post = StatusPostCreateForm()
  return render(request, 'img_website/create.html', {"form":new_post,})

@login_required()
def status_post_update(request, pk):
  user = request.user
  if user.in_group('IMG Member') is False:
    return render(request, 'img_website/restricted.html')
  status_post = StatusPost.objects.get(pk = pk)
  form = StatusPostUpdateForm(instance = status_post)
  if request.method == 'POST':
    form = StatusPostUpdateForm(request.POST, request.FILES, instance = status_post)
    if form.is_valid():
      form.save()
      return redirect(settings.IMG_WEBSITE_BASE_URL+'/dynamic_status/')
  else:
    return render(request, 'img_website/update.html', {"form":form,})

@login_required
@user_passes_test(lambda u: u.groups.filter(name='IMG Member').count() != 0)
def publish_blog_post(request, slug):
  ''' Publish a blogpost '''
  if BlogPost.objects.filter(slug=slug).exists():
    BlogPost.objects.filter(slug=slug).update(state='Published', date=datetime.datetime.now())
    return redirect(settings.IMG_WEBSITE_BASE_URL+'/dynamic_blog/')

@login_required
@user_passes_test(lambda u: u.groups.filter(name='IMG Member').count() != 0)
def publish_works(request, slug):
  ''' Publish a work post '''
  if RecentWorks.objects.filter(slug=slug).exists():
    RecentWorks.objects.filter(slug=slug).update(state='Published', date=datetime.datetime.now())
    return redirect(settings.IMG_WEBSITE_BASE_URL+'/dynamic_works/')

@login_required
@user_passes_test(lambda u: u.groups.filter(name='IMG Member').count() != 0)
def publish_status_post(request, pk):
  ''' Publish a status post '''
  if StatusPost.objects.filter(pk=pk).exists():
    StatusPost.objects.filter(pk=pk).update(state='Published', date=datetime.datetime.now())
    return redirect(settings.IMG_WEBSITE_BASE_URL+'/dynamic_status/')

@login_required
@user_passes_test(lambda u: u.groups.filter(name='IMG Member').count() != 0)
def unpublish_blog_post(request, slug):
  ''' Unpublish a blog post '''
  if BlogPost.objects.filter(slug=slug).exists():
    BlogPost.objects.filter(slug=slug).update(state='Unpublished')
    blogs = BlogPost.objects.filter(state='Published').order_by('-date')
    return redirect(settings.IMG_WEBSITE_BASE_URL+'/dynamic_blog/')

@login_required
@user_passes_test(lambda u: u.groups.filter(name='IMG Member').count() != 0)
def unpublish_works(request, slug):
  ''' Unpublish a work post '''
  if RecentWorks.objects.filter(slug=slug).exists():
    RecentWorks.objects.filter(slug=slug).update(state='Unpublished', date=datetime.datetime.now())
    return redirect(settings.IMG_WEBSITE_BASE_URL+'/dynamic_works/')

@login_required
@user_passes_test(lambda u: u.groups.filter(name='IMG Member').count() != 0)
def unpublish_status_post(request, pk):
  ''' Unpublish a status post '''
  if StatusPost.objects.filter(pk=pk).exists():
    StatusPost.objects.filter(pk=pk).update(state='Unpublished', date=datetime.datetime.now())
    return redirect(settings.IMG_WEBSITE_BASE_URL+'/dynamic_status/')

@login_required
@user_passes_test(lambda u: u.groups.filter(name='IMG Member').count() != 0)
def media(request,path):
  fm = FileManager(basepath=settings.MEDIA_ROOT+'img_website/media/',
      maxspace=500*1024, maxfilesize=50*1024, public_url_base=settings.MEDIA_URL+'img_website/media')
  return fm.render(request,path)
