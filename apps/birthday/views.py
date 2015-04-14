import json as simplejson

from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.models import User,Group
from django.http import HttpResponse
from django.contrib import messages
from django.db.models import Q
from datetime import datetime,date
from notifications.models import Notification
from birthday.models import *
from django.utils.html import escape

def user_dict(user):
  return {
    'username' : user.username,
    'name' : escape(user.name),
    'info' : escape(user.info),
    'photo' : escape(user.photo_url),
  }

def birthday_user_dict(user):
  return {
    'user': user_dict(user),
    'birthdate' : user.birth_date.strftime('%Y-%m-%d %H:%M:%S'),
  }

@login_required
def fetch(request):
  if request.method == 'GET':
    action = request.GET['action']
    pk = request.GET['id']
    group = 'Student' if request.user.groups.filter(name='Student').count() else \
              ('Faculty' if request.user.groups.filter(name='Faculty').count() else None)
    users = User.objects.filter(groups__in = [Group.objects.filter(name = group)[0]])
    if group == 'Student':
      users = users.filter(student__semester = request.user.student.semester)
    else:
      users = users.filter(faculty__department = request.user.semester)
    json = None
    number = int(request.GET['number'])
    if action == 'next':
      pass
    json = simplejson.dumps({'birthday_users':map(birthday_user_dict,users[:number]),'more':int(users.count()>number)})
    return HttpResponse(json,content_type='application/json')


def get_users(user):
  group = 'Student' if user.groups.filter(name='Student').count() else \
            ('Faculty' if user.groups.filter(name='Faculty').count() else None)
  users = []
  if group:
    users = User.objects.filter(groups__in = [Group.objects.filter(name = group)[0]])
  if group == 'Student':
    users = users.filter(
        (Q(student__admission_year = user.student.admission_year)|
        Q(student__groupinfos__in = user.student.groupinfos.all()))&
        Q(birth_date__day = datetime.now().day)&
        Q(birth_date__month = datetime.now().month))
  if group == 'Faculty':
    users = users.filter(faculty__department=user.faculty.department)
    users = users.filter(birth_date_day=datetime.now().day, birth_date__month=datetime.now().month)
  return users

@login_required
def today(request):
  if request.method == 'GET':
    users = get_users(request.user)
    users = list(set(users))
    json = simplejson.dumps({'birthday_users':map(birthday_user_dict,users)})
    return HttpResponse(json,content_type='application/json')

@login_required
def wish(request,username):
  birthday_user = User.objects.get(username=username)
  users = get_users(request.user)
  close = False
  if users.filter(username = username).count() == 0:
    close = True
  else:
    if request.method == 'POST' and request.POST['msg']:
      msg = request.POST['msg']
      bm = BirthdayMessage.objects.create(sender = request.user,receiver = birthday_user,message = msg)
      Notification.save_notification(app='',text=request.user.html_name+' wished you : '+escape(msg),url='/birthday/reply/'+str(bm.pk)+'/',users=[birthday_user], instance=bm)
      messages.info(request,'Your message has been sent to '+birthday_user.first_name);
      close = True
    elif BirthdayMessage.objects.filter(sender = request.user,receiver = birthday_user,date = date.today()).count()>1:
      return render_to_response('birthday/wish.html',{'already_wished':True,'username':username},context_instance=RequestContext(request))
  return render_to_response('birthday/wish.html',{'close':close,'username':username},context_instance=RequestContext(request))

@login_required
def reply(request, message_id):
  bm = BirthdayMessage.objects.get(id = message_id)
  close = False
  if bm.reply == '':
    already_replied = False
  else:
    already_replied = True
  if request.method == 'POST' and request.POST['msg']:
    msg = request.POST['msg']
    bm.reply = msg
    bm.save()
    messages.info(request,'Your message has been sent to '+bm.sender.first_name);
    Notification.save_notification(app='', text=request.user.html_name+' replied you : '+escape(msg), url='', users = [bm.sender.student], instance=bm)
    close = True
    return render_to_response('birthday/reply.html', {'already_replied' : already_replied, 'close' : close}, context_instance = RequestContext(request))
  return render_to_response('birthday/reply.html', {'close' : close, 'already_replied' : already_replied}, context_instance = RequestContext(request))

