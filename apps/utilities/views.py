import datetime
import json

from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.forms.util import ErrorList

from nucleus.models import StudentUserInfo, StudentInfo, WebmailAccount
from nucleus.session import SessionStore
from events.models import EventsUser
from utilities.models import UserSession
from utilities.forms import ProfileFormPrimary, ProfileFormGuardian,\
                            ProfileFormExtra, ChangePasswordForm,\
                            ChangePasswordFirstYearForm, EmailForm,\
                            EventsSubscribeFormGen


@login_required
@user_passes_test(lambda u: u.groups.filter(name='Student').exists())
def edit_profile(request):
  StudentInfo.objects.get_or_create(student=request.user.student)
  student_user_info = StudentUserInfo.objects.get(pk=request.user.pk)
  profileform1 = ProfileFormPrimary(instance=student_user_info)
  profileform2 = ProfileFormGuardian(instance=student_user_info)
  profileform3 = ProfileFormExtra(instance=student_user_info)
  if request.method == 'POST':
    profileform1 = ProfileFormPrimary(request.POST, instance=student_user_info)
    profileform2 = ProfileFormGuardian(request.POST, instance=student_user_info)
    profileform3 = ProfileFormExtra(request.POST, instance=student_user_info)
    if profileform1.is_valid() and profileform2.is_valid() and\
        profileform3.is_valid():
      profileform1.save()
      profileform2.save()
      profileform3.save()
      messages.success(request, "Changes have been saved.")
    else:
      messages.error(request, "Changes couldn't be saved.")
  return render(request, 'utilities/edit_profile.html' ,{
    'form1': profileform1,
    'form2': profileform2,
    'form3': profileform3,
    'student_user_info': student_user_info,
  })


@login_required
def change_password(request):
  user = request.user
  eligible = not WebmailAccount.objects.filter(user=user).exists()
  flag = 0
  message = ''
  form = ChangePasswordForm()
  if request.method == 'POST':
    form = ChangePasswordForm(request.POST)
    if form.is_valid():
      flag = 1
      password = form.cleaned_data['password']
      password1 = form.cleaned_data['password1']
      password2 = form.cleaned_data['password2']
      errors = form._errors.setdefault("__all__", ErrorList())
      if user.check_password(password):
        if password1 == password2:
          user.set_password(password1)
          user.save()
          messages.success(request,'Password changed successfully')
          flag = 2
        else:
          errors.append("New passwords do not match")
      else:
        errors.append("Incorrect current password")
  return render(request, 'utilities/change_password.html', {
      'flag': flag,
      'message': message,
      'form': form,
      'eligible': eligible
  })


@login_required
def change_password_firstyear(request):
  user = request.user
  close = False
  if request.method == 'POST':
    form = ChangePasswordFirstYearForm(request.POST)
    if form.is_valid:
      password1 = request.POST['password1']
      password2 = request.POST['password2']
      if password1 == password2:
        user.set_password(password1)
        user.save()
        messages.success(request,'Password changed successfully')
        close = True
      else:
        messages.error(request,'New passwords do not match')
  else:
    form = ChangePasswordFirstYearForm()
  return render(request, 'utilities/change_password_firstyear.html', {
      'form': form,
      'close': close
  })


@login_required
def person_sessions(request):
  user = request.user
  sessions = UserSession.objects.filter(user=user)
  if request.method == 'POST':
    num = request.POST['num']
    user_session = UserSession.objects.get(pk=num)
    if user_session.user == request.user:
      session_key = user_session.session_key
      user_session.delete()
      session = SessionStore(session_key)
      session.delete()
      messages.success(request, 'The session has been deleted.')
  return render(request, 'utilities/sessions.html',{
    'sessions':sessions,
    'current_session_key': request.session.session_key,
  })


def email(request):
  emailform = EmailForm(initial = {'email':request.user.email})
  events_user, created = EventsUser.objects.get_or_create(user=request.user)
  if created:
    events_user.subscribe_to_calendars()
  EventsSubscribeForm = EventsSubscribeFormGen(request.user)
  events_subscribe_form = EventsSubscribeForm(instance=events_user)
  if request.method == 'POST':
    emailform = EmailForm(request.POST)
    if emailform.is_valid():
      request.user.email = emailform.cleaned_data['email']
      request.user.save()
      events_subscribe_form = EventsSubscribeForm(request.POST,
                                                  instance=events_user)
      events_subscribe_form.save()
      messages.success(request, 'Your preferences have been saved.')
  return render(request, 'utilities/email.html', {
      'events_subscribe_form': events_subscribe_form,
      'emailform': emailform,
      'email_subscribed': events_user.email_subscribed,
  })
