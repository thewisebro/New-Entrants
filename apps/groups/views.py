from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.template import RequestContext
from django.forms.models import modelformset_factory
from django.contrib import messages
from django.contrib.auth.models import User
from django.utils.html import escape
from django.template.defaultfilters import urlize
from events.models import *
import datetime
from django.core.urlresolvers import reverse
from groups import forms
from groups.models import *
from nucleus.models import Student
from api.utils import pagelet_login_required, dialog_login_required

import json

@login_required
def index(request):
  """Home Page"""
  return HttpResponse("Coming Soon!!!")

def get_group_data(group):
  return {
      'username': group.user.username,
      'name': group.short_name,
      'photo': group.user.photo_url,
  }

def get_groups(request):
  groups = Group.objects.filter(is_active=True).order_by('user__name')
  data = {
    'groups': map(lambda g: get_group_data(g), groups),
  }
  return HttpResponse(json.dumps(data), content_type='application/json')

@pagelet_login_required
def group_edit(request,username):
  """
    Editing Group Details
  """
  try:
    group = Group.objects.get(user__username=username)
    groupinfo = GroupInfo.objects.get_or_create(group=group)[0]
  except Group.DoesNotExist as e:
    return render_to_response('groups/group_info.html', {
        'error_msg': 'No group found',
        }, context_instance=RequestContext(request))
  user = request.user
  student = None
  if user.is_authenticated() and user.in_group('Student'):
    student = user.student
  if group.is_active == True or group.admin == student or group.user == user:
    count = group.groupinfo.members.count()
    if group.user == user or group.admin == student:
      can_edit = True
      subscribers = get_subscribers_no(group)
      subscribed = is_user_subscribed(user,group)
      if request.method == 'POST':
        form1 = forms.GroupForm(request.POST,instance=group)
        form2 = forms.GroupInfoForm(request.POST,instance=groupinfo)
        if form1.is_valid() and form2.is_valid():
          form1.save()
          form2.save()
          return HttpResponseRedirect('/groups/'+username+'/')
        else:
          return render_to_response('groups/group_edit.html', {
                  'form1' : form1,
                  'form2' : form2,
                  'group':group,
                  'count':count,
                  'subscribers':subscribers,
                  'can_edit':can_edit,
                  'username':username,
                  'subscribed' : subscribed,
                  'is_active':group.is_active, },
                  context_instance = RequestContext(request))
      else :
        form1 = forms.GroupForm(instance=group)
        form2 = forms.GroupInfoForm(instance=groupinfo)
        return render_to_response('groups/group_edit.html', {
                  'form1' : form1,
                  'form2' : form2,
                  'group':group,
                  'count':count,
                  'subscribers':subscribers,
                  'can_edit':can_edit,
                  'username':username,
                  'subscribed':subscribed,
                  'is_active':group.is_active},
                  context_instance = RequestContext(request))
    else:
      return HttpResponseRedirect('/groups/'+username)
  else:
    return HttpResponseRedirect('/')

r"""
def get_subscribers_no(group):
  if group.is_active :
    cal,created = Calendar.objects.get_or_create(name = group.user.username)
    if created:
      cal.users.add(group.user)
      cal.users.add(group.admin.user)
      cal.cal_type = 'GRP'
      cal.save()
    subscribers = cal.eventsuser_set.count()
    return subscribers
  else:
    return 0

def is_user_subscribed(user,group):
  if Calendar.objects.filter(name = group.user.username,cal_type = 'GRP').exists():
    eventuser = EventsUser.objects.get_or_create(user = user)[0]
    grp_cal = Calendar.objects.get(name = group.user.username)
    subscribed = False
    if eventuser.calendars.filter(name = grp_cal.name,cal_type='GRP').exists():
      subscribed = True
    return subscribed
  else:
    return False
"""

def get_subscribers_no(group):
  return group.groupinfo.subscribers.count()

def is_user_subscribed(user,group):
  return group.groupinfo.subscribers.filter(username = user.username).exists()

def group_details(request,username):
  try:
    group = Group.objects.get(user__username = username)
  except Group.DoesNotExist as e:
    return render_to_response('groups/index.html', {
        'error_msg': 'No group found',
        }, context_instance=RequestContext(request))
  user = request.user
  student = None
  if user.is_authenticated() and user.in_group('Student'):
    student = user.student
  if group.is_active == True or group.user == user or group.admin == student:
    can_edit = False
    subscribers = get_subscribers_no(group)
    subscribed = is_user_subscribed(user,group)
    if group.user == user or group.admin == student:
      can_edit = True
    groupinfo = GroupInfo.objects.get_or_create(group=group)[0]
    m = Membership.objects.filter(groupinfo=groupinfo)
    count = group.groupinfo.members.count()
    return render_to_response('groups/index.html', {
        'group' : group,
        'can_edit' : can_edit,
        'membership' : m,
        'count' : count,
        'subscribers':subscribers,
        'username':username,
        'subscribed':subscribed,
        }, context_instance=RequestContext(request))
  else:
    return HttpResponseRedirect('/')

def group_events(request,username):
  try:
    group = Group.objects.get(user__username = username)
  except Group.DoesNotExist as e:
    return render_to_response('groups/index.html', {
        'error_msg': 'No group found',
        }, context_instance=RequestContext(request))
  user = request.user
  student = None
  if user.is_authenticated() and user.in_group('Student'):
    student = user.student
  if group.is_active == True or group.user == user or group.admin == student:
    can_edit = False
    subscribers = get_subscribers_no(group)
    subscribed = is_user_subscribed(user,group)
    if group.user == user or group.admin == student:
      can_edit = True
    groupinfo = GroupInfo.objects.get_or_create(group=group)[0]
    m = Membership.objects.filter(groupinfo=groupinfo)
    count = group.groupinfo.members.count()
    return render_to_response('groups/events.html', {
        'group' : group,
        'can_edit' : can_edit,
        'membership' : m,
        'count' : count,
        'subscribers':subscribers,
        'username':username,
        'subscribed':subscribed,
        }, context_instance=RequestContext(request))
  else:
    return HttpResponseRedirect('/')

def group_members(request,username):
  try:
    group = Group.objects.get(user__username = username)
  except Group.DoesNotExist as e:
    return render_to_response('groups/group_members.html', {
        'error_msg': 'No group found',
        }, context_instance=RequestContext(request))
  user = request.user
  student = None
  if user.is_authenticated() and user.in_group('Student'):
    student = user.student
  if group.is_active == True or group.user == user or group.admin == student:
    can_edit = False
    subscribers = get_subscribers_no(group)
    subscribed = is_user_subscribed(user,group)
    if group.user == user or group.admin == student:
      can_edit = True
    groupinfo = GroupInfo.objects.get_or_create(group=group)[0]
    m = Membership.objects.filter(groupinfo=groupinfo).order_by('student__admission_year','student__user__name')
    count = group.groupinfo.members.count()
    return render_to_response('groups/group_members.html', {
        'group' : group,
        'can_edit' : can_edit,
        'membership' : m,
        'count' : count,
        'subscribers':subscribers,
        'username':username,
        'subscribed':subscribed,
        }, context_instance=RequestContext(request))
  else:
    return HttpResponseRedirect('/')


@dialog_login_required
def member_add(request, username):
  """
  Adds a member to the group.
  """
  try:
    group = Group.objects.get(user__username=username)
  except Group.DoesNotExist as e:
    return render_to_response('groups/member_add.html', {
        'error_msg': 'No group found',
        'group' : group,
        }, context_instance=RequestContext(request))
  user = request.user
  student = None
  if user.is_authenticated() and user.in_group('Student'):
    student = user.student
  groupinfo = GroupInfo.objects.get(group=group)
  MemberAddForm = forms.MemberAddFormGen(groupinfo)
  page_info = 'Add a Member'
  if group.user == user or group.admin == student:
    if request.method == 'POST':
      form = MemberAddForm(request.POST,instance=groupinfo)
      if form.is_valid():
        username = form.cleaned_data['username'].strip()
        post = form.cleaned_data['post']
        try:
          user = User.objects.get(username=username)
          student_to_add = user.student
        except User.DoesNotExist as e:
          form = MemberAddForm(instance=groupinfo)
          return render_to_response('groups/member_add.html', {
              'msg': 'Specified student not found',
              'form' : form,
              'group' : group,
              'page_info':page_info,
              }, context_instance=RequestContext(request))
        if student_to_add not in groupinfo.members.all():
          postobj = groupinfo.posts.get_or_create(post_name=post)[0]
          membership = Membership.objects.create(student=user.student,post=postobj,groupinfo=groupinfo)
          membership.save()
          msg = 'Member added successfully'
          messages.success(request,msg)
        else:
          msg = "Specified member already exist"
          messages.error(request,msg)
        form = MemberAddForm(instance=groupinfo)
        return render_to_response('groups/member_add.html', { 'form':form, 'group':group, 'page_info':page_info}, context_instance = RequestContext(request))
      else:
        msg = 'Please enter a correct Enrollment No.'
        messages.error(request,msg)
        form = MemberAddForm(instance=groupinfo)
        return render_to_response('groups/member_add.html', {
        'group':group,'page_info':page_info,'form':form}, context_instance = RequestContext(request))
    else :
      if groupinfo.posts.count() == 0:
        groupinfo.posts.create(post_name="Member")
      form = MemberAddForm(instance=groupinfo)
      return render_to_response('groups/member_add.html', {
        'form' : form,'group':group,'page_info':page_info}, context_instance = RequestContext(request))
  else:
    return HttpResponseRedirect('/groups/'+username)

@dialog_login_required
def member_delete(request,username):
  """
  Remove members
  """
  try:
    group = Group.objects.get(user__username=username)
  except Group.DoesNotExist as e:
    return render_to_response('groups/member_delete.html', {
        'error_msg': 'No Group found',
        'group' : group,
        }, context_instance=RequestContext(request))
  user = request.user
  student = None
  if user.is_authenticated() and user.in_group('Student'):
    student = user.student
  groupinfo = GroupInfo.objects.get(group=group)
  choices = groupinfo.members.all()
  form = forms.MemberDeleteForm(choices)
  page_info = 'Delete members'
  if group.user == user or group.admin == student:
    if request.method == 'POST':
      members_list = request.POST.getlist('members')
      check = True
      for member_to_be_deleted in members_list :
        student = Student.objects.get(pk=str(member_to_be_deleted))
        m = Membership.objects.get(student=student,groupinfo=groupinfo)
        if m :
          m.delete()
        else:
          check = False
      if check is True:
        msg='Deletion Successful'
        messages.success(request,msg)
      else:
        msg='Some error occured'
        messages.error(request,msg)
      form = forms.MemberDeleteForm(choices)
      return render_to_response('groups/member_delete.html', {
        'group':group,'form':form,'page_info':page_info}, context_instance = RequestContext(request))
    else :
      return render_to_response('groups/member_delete.html', {
        'form' : form,'group':group,'page_info':page_info}, context_instance = RequestContext(request))
  else:
    return HttpResponseRedirect('/groups/'+username)

@dialog_login_required
def member_add_multiple(request,username):
  """
  Adds multiple members by assigning them default post..
  """
  try:
    group = Group.objects.get(user__username=username)
  except Group.DoesNotExist as e:
    return render_to_response('groups/member_add_multiple.html', {
        'error_msg': 'No group found',
        'group' : group,
        }, context_instance=RequestContext(request))
  user = request.user
  student = None
  if user.is_authenticated() and user.in_group('Student'):
    student = user.student
  groupinfo = GroupInfo.objects.get(group=group)
  page_info="Add Multiple Members"
  if group.user == user or group.admin == student:
    if request.method == 'POST' :
      form = forms.MemberAddMultiple(request.POST)
      if form.is_valid() :
        comma_separated_list = form.cleaned_data['username_list']
        usernames = []
        for i in comma_separated_list.split(','):
          usernames.append(i.replace(" ","").replace("\r","").replace("\n",""))
        status = []
        name = []
        for username in usernames:
          try:
            user_to_add = User.objects.get(username=username)
          except User.DoesNotExist as e:
            result = ': Student not Found/Incorrect Enrollment no.'
            status.append(result)
            continue
          student_to_add = user_to_add.student
          if student_to_add:
            if student_to_add not in groupinfo.members.all():
              postobj = groupinfo.posts.get_or_create(post_name='Member')[0]
              membership = Membership.objects.create(student=student_to_add,post=postobj,groupinfo=groupinfo)
              membership.save()
              result = ': Added successfully'
            else:
              result = ': Student already a member of the group'
          else:
            result = ": Student not found/Incorrect Enrollment number."
          status.append(result)
        results = zip(usernames,status)
        form = forms.MemberAddMultiple()
        return render_to_response('groups/member_add_multiple.html', {
              'results': results,
              'form' :form,
              'group':group,
              'page_info':page_info,
              }, context_instance=RequestContext(request))
      else:
        form = forms.MemberAddMultiple()
        return render_to_response('groups/member_add_multiple.html', {
                'msg': 'Some error occured.Please enter correctly..',
                'form' : form,
                'group' :group,
                'page_info':page_info,
                }, context_instance=RequestContext(request))
    else:
      form = forms.MemberAddMultiple()
      return render_to_response('groups/member_add_multiple.html', {
        'form' : form,
        'group' : group,
        'page_info':page_info,
        'msg':'Please enter comma seperated enrollment number list.Their post will be defaulted to "Member" '},
        context_instance = RequestContext(request))
  else:
    return HttpResponseRedirect('/groups/'+username)

@dialog_login_required
def admin_change(request, username):
  """
    Changes Admin of a Group
  """
  try:
    group = Group.objects.get(user__username=username)
  except Group.DoesNotExist as e:
    return render_to_response('groups/admin_change.html', {
        'error_msg': 'No group found',
        }, context_instance=RequestContext(request))
  user = request.user
  student = None
  if user.is_authenticated() and user.in_group('Student'):
    student = user.student
  groupinfo = GroupInfo.objects.get(group=group)
  form = forms.AdminChangeFormGen(groupinfo)
  page_info = 'Change Admin'
  if group.admin == student or group.user == user:
    if request.method == 'POST':
      form = form(request.POST)
      if form.is_valid() :
        member = form.cleaned_data['student']
        username = str(member).rpartition(':')[0].partition(':')[2]
        u = User.objects.get(username=username)
        new_admin = u.student
        if group.admin <> new_admin:
          if Calendar.objects.filter(name=group.user.username,cal_type='GRP').exists():
            cal = Calendar.objects.get(name=group.user.username,cal_type='GRP')
            cal.users.add(new_admin.user)
            if group.admin:
              cal.users.remove(group.admin.user)
          group.admin = new_admin
          group.save()
          msg = 'Successfully changed'
          messages.success(request,msg)
        else:
          msg='Specified Student is already admin of the group.'
          messages.error(request,msg)
        return render_to_response('groups/admin_change.html', {
              'form' : form,
              'group' : group,
              'page_info':page_info,
              }, context_instance=RequestContext(request))
    else :
      return render_to_response('groups/admin_change.html', {
        'form' : form,'group':group,'page_info':page_info,}, context_instance = RequestContext(request))
  return HttpResponseRedirect('/groups/'+username)


@dialog_login_required
def post_add(request,username):
  """
  Adds a post available for a particular group
  """
  try:
    group = Group.objects.get(user__username=username)
  except Group.DoesNotExist as e:
    return render_to_response('groups/post_add.html', {
        'error_msg': 'No group found',
        'group' : group,
        }, context_instance=RequestContext(request))
  user = request.user
  student = None
  if user.is_authenticated() and user.in_group('Student'):
    student = user.student
  groupinfo = GroupInfo.objects.get(group=group)
  page_info = 'Add a Post'
  if group.user == user or group.admin == student:
    if request.method == 'POST':
      form = forms.PostAdd(request.POST)
      if form.is_valid() :
        postname = form.cleaned_data['postname'].strip()
        if not groupinfo.posts.filter(post_name=postname).exists():
          post_to_save = groupinfo.posts.get_or_create(post_name=postname)[0]
          msg = 'Post added successfully'
          messages.success(request,msg)
        else:
          msg = "Specified post already exist"
          messages.error(request,msg)
        form = forms.PostAdd()
        return render_to_response('groups/post_add.html', { 'msg':msg,'form':form, 'group':group, 'page_info':page_info }, context_instance = RequestContext(request))
      else:
        msg = 'Please enter a valid Post'
        messages.error(request,msg)
        return render_to_response('groups/post_add.html', {
        'msg' : msg, 'group':group, 'page_info':page_info,}, context_instance = RequestContext(request))
    else :
      form = forms.PostAdd()
      return render_to_response('groups/post_add.html', {
        'form' : form,'group':group, 'page_info':page_info}, context_instance = RequestContext(request))
  else:
    return HttpResponseRedirect('/groups/'+username)

@dialog_login_required
def post_delete(request,username):
  """
  Deletes a post and defaults the post of the affected members.
  """
  try:
    group = Group.objects.get(user__username=username)
  except Group.DoesNotExist as e:
    return render_to_response('groups/post_delete.html', {
        'error_msg': 'No group found',
        'group' : group,
        }, context_instance=RequestContext(request))
  user = request.user
  student = None
  if user.is_authenticated() and user.in_group('Student'):
    student = user.student
  groupinfo = GroupInfo.objects.get(group=group)
  page_info = 'Delete Posts'
  choices = groupinfo.posts.all().exclude(post_name="Member")
  form = forms.PostDeleteForm(choices)
  if group.user == user or group.admin == student:
    if request.method == 'POST':
      posts = request.POST.getlist('posts')
      for post in posts:
        postobj = groupinfo.posts.filter(pk=str(post))[0]
        members = Membership.objects.filter(post=postobj,groupinfo=groupinfo)
        for member in members:
          newpost = groupinfo.posts.get_or_create(post_name="Member")[0]
          member.post = newpost
          member.save()
        postobj.delete()
      msg = "Successfully deleted"
      messages.success(request,msg)
      return render_to_response('groups/post_delete.html', {
        'form' : form,'group':group, 'page_info':page_info,}, context_instance = RequestContext(request))
    else :
      return render_to_response('groups/post_delete.html', {
        'form' : form,'group':group, 'page_info':page_info,}, context_instance = RequestContext(request))
  else:
    return HttpResponseRedirect('/groups/'+username)

@dialog_login_required
def post_change(request,username):
  """
  Changes the post of the selected member
  """
  try:
    group = Group.objects.get(user__username=username)
  except Group.DoesNotExist as e:
    return render_to_response('groups/post_change.html', {
        'error_msg': 'No group found',
        'group' : group,
        }, context_instance=RequestContext(request))
  user = request.user
  student = None
  if user.is_authenticated() and user.in_group('Student'):
    student = user.student
  groupinfo = GroupInfo.objects.get(group=group)
  page_info = 'Change Post'
  form = forms.PostChangeFormGen(groupinfo)
  if group.user == user or group.admin == student:
    if request.method == 'POST':
      form = form(request.POST)
      if form.is_valid() :
        member = form.cleaned_data['student']
        postname = form.cleaned_data['post']
        username = str(member).rpartition(':')[0].partition(':')[2]
        print username
        postobj = groupinfo.posts.get_or_create(post_name=postname)[0]
        u = User.objects.get(username=username)
        p = u.student
        m = Membership.objects.filter(student=p,groupinfo=groupinfo)
        a = m[0]
        a.post = postobj
        a.save()
        msg = "Post change successfull"
        messages.success(request,msg)
        return render_to_response('groups/post_change.html', {
              'form' : form,
              'group' : group,
              'page_info': page_info,
              }, context_instance=RequestContext(request))

    else :
      return render_to_response('groups/post_change.html', {
        'form' : form,'group':group, 'page_info':page_info,}, context_instance = RequestContext(request))
  else:
    return HttpResponseRedirect('/groups/'+username)

@pagelet_login_required
def subscriber(request,username):
  """
    Subscribe/Unscubscribes a student to a group.
  """
  try:
    group = Group.objects.get(user__username=username)
  except Group.DoesNotExist as e:
    return render_to_response('groups/index.html', {
        'error_msg': 'No group found',
        'group' : group,
        }, context_instance=RequestContext(request))
  if request.is_ajax() and request.method == 'POST' and group.is_active:
    user = request.user
    student = None
    if user.is_authenticated() and user.in_group('Student'):
      student = user.student
    subscribed = request.POST['subscribed']
    msg='filler'
    if subscribed == 'False':
      if not is_user_subscribed(user,group):
        group.groupinfo.subscribers.add(user)
        msg = 'Successfully subscribed to '+str(group.name)
      else:
        msg = 'Already a Subscriber'
    else:
      group.groupinfo.subscribers.remove(user)
      msg = 'Successfully unsubscribed from '+str(group.name)
    subscribers = get_subscribers_no(group)
    messages.success(request,msg )
    json = json.dumps({'subscribers':subscribers})
    return HttpResponse(json,content_type='application/json')
  else:
    return HttpResponseRedirect('/groups/'+username)

@pagelet_login_required
def activate(request,username):
  """
    Activates the group's account
  """
  try:
    group = Group.objects.get(user__username=username)
  except Group.DoesNotExist as e:
    return render_to_response('groups/index.html', {
        'error_msg': 'No group found',
        'group' : group,
        }, context_instance=RequestContext(request))
  user = request.user
  student = None
  if user.is_authenticated() and user.in_group('Student'):
    student = user.student
  if group.user == user or group.admin == student:
    group.is_active = True
    group.save()
    cal,created = Calendar.objects.get_or_create(name = group.user.username)
    if created:
      cal.users.add(group.user)
      if group.admin:
        cal.users.add(group.admin.user)
      cal.cal_type = 'GRP'
      cal.save()
      cal.eventsuser_set.add(*list(EventsUser.objects.all()))
    messages.success(request,'Your group has been successfully activated')
    return HttpResponseRedirect(reverse('groups.views.group_details',args=[username]))
  else:
    return HttpResponseRedirect('/groups/'+username)

def group_activity(request,username):
  try:
    group = Group.objects.get(user__username = username)
  except Group.DoesNotExist as e:
    return render_to_response('groups/index.html', {
        'error_msg': 'No group found',
        }, context_instance=RequestContext(request))
  user = request.user
  student = None
  if user.is_authenticated() and user.in_group('Student'):
    student = user.student
  if group.is_active == True or group.user == user or group.admin == student:
    can_edit = False
    subscribers = get_subscribers_no(group)
    subscribed = is_user_subscribed(user,group)
    if group.user == user or group.admin == student:
      can_edit = True
    groupinfo = GroupInfo.objects.get_or_create(group=group)[0]
    m = Membership.objects.filter(groupinfo=groupinfo)
    count = group.groupinfo.members.count()
    if request.method == 'POST' and can_edit:
      text = request.POST['text']
      if text:
        GroupActivity.objects.create(group = group,text = text)
    return render_to_response('groups/activity.html', {
        'group' : group,
        'can_edit' : can_edit,
        'membership' : m,
        'count' : count,
        'subscribers':subscribers,
        'username':username,
        'subscribed':subscribed,
        }, context_instance=RequestContext(request))
  else:
    return HttpResponseRedirect('/')

def activity_dict(activity):
  return {
    'id' : activity.pk,
    'datetime' : activity.datetime_created.strftime('%Y-%m-%d %H:%M:%S'),
    'text' : urlize(escape(activity.text)).replace('\n','<br>'),
  }

def fetch_activities(request):
  action = request.GET['action']
  group_username = request.GET['group_username']
  pk = request.GET['id']
  json_data = None
  number = int(request.GET['number'])
  group = Group.objects.get(user__username = group_username)
  if action == 'first':
    activities = group.groupactivity_set.all()
  elif action == 'next':
    activities = group.groupactivity_set.filter(pk__lt = pk)
  json_data = json.dumps({'activities':map(activity_dict,activities[:number]),'more':int(activities.count()>number)})
  return HttpResponse(json_data,content_type='application/json')

