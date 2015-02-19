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
from django.views.generic.base import TemplateView

from zipfile import ZipFile
from django.contrib import messages
from placement.utils import handle_exc
import datetime
import os, xlwt
import logging

import cStringIO as StringIO
from internship.models import *
from internship import forms 
from nucleus.models import Student, Branch, StudentInfo, WebmailAccount
from placement.models import InternshipInformation, ProjectInformation
from placement.policy import current_session_year
import logging
from django.conf import settings
import datetime

# Permission denied page. User will be redirected to this page if he fails the user_passes_test.
login_url = '/internship/'
l=logging.getLogger('internship')

# Forum views
@login_required
def forum(request, forum_type, page_no = None) :
  """
  Show all the posts to the technical/placement forums.
  It saves the reply to a post also.
  """
  #l.info(request.user.username+' :tried to view the forum view')

 
  from django.core.mail import send_mail
  try:
    if request.method == 'POST' :
      if request.POST['content']=="":
        messages.error(request, 'An empty reply cannot be posted')
        return HttpResponseRedirect(reverse('internship.views_forum.forum', args=[ forum_type ]))
      if request.session.get('person'):
        person = request.session.get('person')
        post = ForumPost.objects.get(pk = request.POST['post_id'])
        reply = ForumReply(post = post,
                         enrollment_no = person.user.username,
                         person_name = person.name,
                         content = request.POST['content'],
                        )
        reply.save()
        l.info(request.user.username+' : tried to post a reply on forum')
        messages.success(request, "Forum Post successful")
      elif request.session.get('user'):
        user = request.session.get('user')
        #if user.groups.filter(name = 'Placement Admin').exists():
        post = ForumPost.objects.get(pk = request.POST['post_id'])
        reply = ForumReply(post = post,
                         enrollment_no = '00000000',
                         person_name = 'Placement Admin',
                         content = request.POST['content'],
                        )
        reply.save()
        l.info(request.user.username+' : tried to post a reply on forum')
        messages.success(request, "Forum Post successful")
      #l.info(request.user.username+' :tried to view the forum')  
      return HttpResponseRedirect('')
    if not page_no :
      page_no = 1
    else :
      page_no = int(page_no)
    post_headers = ForumPost.objects.filter(forum_type = forum_type).order_by('-date')
    pages = range(1,(post_headers.count()+19)/10)
    # If only a single page, do not show paging
    if len(pages) == 1 :
      pages = None
    l.info(request.user.username+' :tried to view the forum view page no'+str(page_no))
    post_headers = post_headers[(page_no-1)*10:page_no*10]
    replies = []
    for post in post_headers :
      replies.append(ForumReply.objects.filter(post = post).order_by('date'))
    posts = zip(post_headers, replies)
    return render_to_response('internship/forums_view.html', {
      'forum_type' : forum_type,
      'posts' : posts,
      'page_no' : page_no,
      'pages' : pages
      }, context_instance = RequestContext(request))
  except Exception as e:
    l.info(request.user.username +': encountered exception when viewing forum view')
    l.exception(e)
    return handle_exc(e, request) 

@login_required
def forum_post(request) :
  """
  Adds a new Post to the forum.
  """
  
  try:
    if request.method == 'POST' :
      if request.POST['title']=="":
        messages.error(request, 'Please fill in the Question before submitting.')
        return HttpResponseRedirect(reverse('internship.views_forum.forum', args=[ request.POST['forum_type'] ]))
      elif request.session.get('person'):
        person = request.session.get('person')
        # DONE?: TODO : You may want to convert department_name to a human readable format.
        post = ForumPost(enrollment_no = person.user.username,
                     person_name = person.name,
                     discipline_name = person.branch.name,
                     department_name = person.branch.get_department_display(),
                     title = request.POST['title'],
                     content = request.POST['content'],
                     forum_type = request.POST['forum_type']
                     )
        
        post.save()
        l.info(request.user.username+' :added a new post to the forum ')
      elif request.session.get('user') :
        post = ForumPost(enrollment_no = '00000000',
                      person_name = 'Placement Admin',
                      discipline_name = 'Admin',
                      department_name = 'Admin',
                      title = request.POST['title'],
                      content = request.POST['content'],
                      forum_type = request.POST['forum_type']
                      )
        post.save()
      try:  
        person = request.session['person']
        email_id=PersonIdEnrollmentNoMap.objects.get(enrollment_no=request.user.username).person_id
        forum_type=request.POST['forum_type']
        if(forum_type=="T"):
          subject_mail="New post on Internship Technical forum by "+ person.name   
        elif(forum_type=="P"):
          subject_mail="New post on Internship forum by "+ person.name        
        content_mail="Post Title: "+request.POST['title']+'\n'+"Post Content: "+request.POST['content']
        from django.core.mail import send_mail
        forum_type=request.POST['forum_type']
        if(forum_type=="T"):
          send_mail(subject_mail, content_mail,'img@iitr.ernet.in' , ['img.placement@gmail.com'])
        elif(forum_type=="P"):
          send_mail(subject_mail, content_mail, 'img@iitr.ernet.in' , ['placement.iitr@gmail.com'])
        messages.success(request, 'You posted successfully on the forum')
      
      except Exception as e:
        logger.info(request.user.username+': got an exception in mailer block during forum post')
        logger.exception(e)
        return handle_exc(e, request)

      l.info(request.user.username+' : added a new post to the forum')
      
      return HttpResponseRedirect('/internship/forum/' + request.POST['forum_type'] + '/')
  except Exception as e:
    l.info(request.user.username +': encountered exception when adding a new post to the forum')
    l.exception(e)
    return handle_exc(e, request)

