import datetime
import json
import hashlib
import random

from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.forms.util import ErrorList
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,redirect
from django.utils import timezone
from django.core.mail import send_mail

from nucleus.models import StudentUserInfo, StudentInfo, WebmailAccount
from nucleus.session import SessionStore
from events.models import EventsUser
from api.utils import pagelet_login_required, dialog_login_required
from utilities.models import UserSession, PasswordCheck, UserEmail
from utilities.forms import ProfileFormPrimary, ProfileFormGuardian,\
    ProfileFormExtra, ChangePasswordForm, ChangePasswordFirstYearForm,\
    EmailForm, EventsSubscribeFormGen, GenProfileForm, PasswordCheckForm,\
    UserEmailForm


@pagelet_login_required
def edit_profile(request):
  if request.user.in_group('Student'):
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
    return render(request, 'utilities/pagelets/edit_profile.html', {
      'form': profileform1,
      'form2': profileform2,
      'form3': profileform3,
    })
  else:
    profileform = GenProfileForm(instance=request.user)
    if request.method == 'POST':
      profileform = GenProfileForm(request.POST, instance=request.user)
      if profileform.is_valid():
        profileform.save()
        messages.success(request, "Changes have been saved.")
      else:
        messages.error(request, "Changes couldn't be saved.")
    return render(request, 'utilities/pagelets/edit_profile.html', {
      'form': profileform,
    })


@pagelet_login_required
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
  return render(request, 'utilities/pagelets/change_password.html', {
      'flag': flag,
      'message': message,
      'form': form,
      'eligible': eligible
  })


@dialog_login_required
def change_password_firstyear(request):
  user = request.user
  if request.method == 'POST':
    form = ChangePasswordFirstYearForm(request.POST)
    if form.is_valid():
      password1 = request.POST['password1']
      password2 = request.POST['password2']
      if password1 == password2:
        user.set_password(password1)
        user.save()
        messages.success(request,'Password changed successfully')
        return HttpResponseRedirect(reverse('close_dialog', kwargs={
              'dialog_name': 'pass_change'
        }))
      else:
        messages.error(request,'New passwords do not match')
  else:
    form = ChangePasswordFirstYearForm()
  return render(request, 'utilities/dialogs/change_password_firstyear.html', {
      'form': form,
  })


@pagelet_login_required
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
  return render(request, 'utilities/pagelets/sessions.html',{
    'sessions':sessions,
    'current_session_key': request.session.session_key,
  })

@pagelet_login_required
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
  return render(request, 'utilities/pagelets/email.html', {
      'events_subscribe_form': events_subscribe_form,
      'emailform': emailform,
      'email_subscribed': events_user.email_subscribed,
  })

@pagelet_login_required
def email_verify(request):
  primary_entry = None
  if request.method == 'POST':
    if 'primary' in request.POST or 'primary_2' in request.POST:
      entry = UserEmail.objects.get(pk= request.POST['id'])
      authenticated = PasswordCheck.exists_for(user=entry.user,\
          service='email_auth')
      if authenticated:
        if entry.verified:
          request.user.email = entry.email
          request.user.save()
        else:
          messages.error(request,"Email need to be verified first")
      else:
        if 'primary' in request.POST:
          primary_entry = entry

    if 'delete' in request.POST:
      entry = UserEmail.objects.get(pk= request.POST['id'])
      if entry.email== request.user.email:
        messages.error(request,"Primary Email addresses can't be deleted")
      else:
        entry.delete()

    if 'verify' in request.POST:
      entry= UserEmail.objects.get(pk= request.POST['id'])
      salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
      confirmation_key = hashlib.sha1(salt+entry.email).hexdigest()
      if entry.last_datetime_created.date() == datetime.date.today():
        entry.verify_num= entry.verify_num + 1
      else:
        entry.verify_num = 1
      if entry.verify_num < 4 :
        entry.confirmation_key= confirmation_key
        entry.last_datetime_created = datetime.datetime.today()
        entry.save()
        email_subject = 'Account confirmation'
        email_body = " To verify your email address, click this link within" + \
                     " 48hours http://channeli.in/#settings/email_auth/"+\
                     "?confirm_key=%s" % (confirmation_key)
        send_mail(email_subject, email_body,'channeli@iitr.ac.in',[entry.email],\
             fail_silently=False)
        email1_subject = 'New Email address added for your channeli account.'
        email1_body = "A new Email address %s has been added to your"+\
                       " channeli account." % (entry.email)
        send_mail(email1_subject, email1_body, 'channeli@iitr.ac.in',\
            [request.user.email], fail_silently=False)

        messages.success(request,"A verification link has been sent"+\
            " to your email address.")
      else:
        messages.error(request,"Max limit of verification for this email" +\
            " has been reached for today")

    if 'submission' in request.POST:
      useremailform = UserEmailForm(request.POST)
      if useremailform.is_valid():
        email = useremailform.cleaned_data['email']
        if UserEmail.objects.filter(user=request.user).filter(email\
            =email).count():
          messages.error(request,'This email has already been submitted.')
        else:
          salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
          confirmation_key = hashlib.sha1(salt+email).hexdigest()
          new_entry = UserEmail(user=request.user,email=email, confirmation_key\
              =confirmation_key, last_datetime_created=datetime.datetime.today(),\
              verify_num=1)
          new_entry.save()
          email_subject = 'Account confirmation'
          email_body = " To verify your email address, click this link within" +\
                        " 48hours http://channeli.in/#settings/email_auth/"+\
                        "?confirm_key=%s" % (confirmation_key)
          send_mail(email_subject, email_body, 'channeli@iitr.ac.in',[email],\
              fail_silently=False)
          email1_subject = 'New Email address added for your channeli account.'
          email1_body = "A new Email address %s has been added to your"+\
                         " channeli account." % (email)
          send_mail(email1_subject, email1_body, 'channeli@iitr.ac.in',\
              [request.user.email], fail_silently=False)
          messages.success(request,"A verification link has been sent"+\
              " to your email address.")

  if 'confirm_key' in request.GET:
    confirmation_key = request.GET['confirm_key']
    try:
      email_profile = UserEmail.objects.filter(user=\
          request.user).get(confirmation_key=confirmation_key)
      if email_profile.last_datetime_created + datetime.timedelta(2) < timezone.now():
        messages.error(request,"The verification-key expired.")
      else:
        email_profile.verified = True
        email_profile.save()
        messages.success(request,"Your email has been verified for this account.")
    except UserEmail.DoesNotExist:
      messages.error(request,"This link is no longer active for verification.")

  useremailform = UserEmailForm()
  if not UserEmail.objects.filter(user=request.user).exists():
    if request.user.email:
      useremail = UserEmail()
      useremail.user = request.user
      useremail.email = request.user.email
      useremail.verified= False
      useremail.last_datetime_created = datetime.datetime.today()
      useremail.save()
  emails_for_user = UserEmail.objects.filter(user=request.user)
  lastdate = timezone.now() - datetime.timedelta(2)
  verifiable_emails = emails_for_user.filter(last_datetime_created__gte=\
      lastdate).filter(verified=False)
  primary_email = request.user.email
  count = emails_for_user.count()
  return render(request,'utilities/pagelets/email_auth.html',{
      'useremailform': useremailform,
      'emails_for_user': emails_for_user,
      'primary_email':primary_email,
      'count':count,
      'verifiable_emails':verifiable_emails,
      'primary_entry': primary_entry,
  })



@dialog_login_required
def password_check(request):
  user = request.user
  if request.method == 'POST':
    service = request.GET['service']
    seconds = int(request.GET['seconds'])
    form = PasswordCheckForm(request.POST)
    if form.is_valid():
      password = request.POST['password']
      if user.check_password(password):
        PasswordCheck.objects.create(user=user, service=service,
                        seconds=seconds)
        return HttpResponseRedirect(reverse('close_dialog', kwargs={
              'dialog_name': 'pass_check'
        }))
      else:
        messages.error(request,'Password didn\'t match.')
  else:
    form = PasswordCheckForm()
  return render(request, 'utilities/dialogs/password_check.html', {
      'form': form,
  })
