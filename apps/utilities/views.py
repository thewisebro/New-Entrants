import datetime
import simplejson
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

from nucleus.models import StudentUserInfo, StudentInfo, WebmailAccount, User
from nucleus.session import SessionStore
from events.models import EventsUser
from notices.models import NoticeUser, Category
from notices.constants import MAIN_CATEGORIES_CHOICES
from api.utils import pagelet_login_required, dialog_login_required
from utilities.models import UserSession, PasswordCheck, UserEmail, PasswordReset
from nucleus.models import *
from django.db.models import Q
from utilities.forms import ProfileFormPrimary, ProfileFormGuardian,\
    ProfileFormExtra, ChangePasswordForm, ChangePasswordFirstYearForm,\
    EmailForm, EventsSubscribeFormGen,NoticesSubscribeForm, GenProfileForm, PasswordCheckForm,\
    UserEmailForm, PasswordResetRequestForm, PasswordResetForm
from utilities.utils import *

import logging
logger = logging.getLogger('email_verify_logger')


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
  emailform = EmailForm(instance=request.user)
  events_user, created = EventsUser.objects.get_or_create(user=request.user)
  notice_user = NoticeUser.objects.get_or_create(user=request.user)[0]
  if created:
    events_user.subscribe_to_calendars()
  EventsSubscribeForm = EventsSubscribeFormGen(request.user)
  events_subscribe_form = EventsSubscribeForm(instance=events_user)
  notices_subscribe_form = NoticesSubscribeForm(instance=notice_user)
  if request.method == 'POST':
    emailform = EmailForm(request.POST)
    if emailform.is_valid():
      if not request.user.email:
        request.user.email = emailform.cleaned_data['email']
        request.user.save()
      events_subscribe_form = EventsSubscribeForm(request.POST,
                                                  instance=events_user)
      events_subscribe_form.save()
      clicked_categories = request.POST.getlist('categories')
      for main_cat in clicked_categories:
        target_categories = Category.objects.filter(main_category=main_cat)
        for sub_cat in target_categories:
          notice_user.categories.add(sub_cat)
      all_categories=[a[0] for a in MAIN_CATEGORIES_CHOICES]
      for main_cat in all_categories:
          if main_cat not in clicked_categories:
            target_categories = Category.objects.filter(main_category=main_cat)
            for sub_cat in target_categories:
              notice_user.categories.remove(sub_cat)

      notice_user.save()
      notices_subscribe_form = NoticesSubscribeForm(request.POST,
                                                  instance=notice_user)
      notices_subscribe_form.save()
      messages.success(request, 'Your preferences have been saved.')

  categories = notice_user.categories.all()
  main_categories=[]
  for category in categories:
    if category.main_category not in main_categories:
      main_categories.append(category.main_category)

  return render(request, 'utilities/pagelets/email.html', {
      'events_subscribe_form': events_subscribe_form,
      'emailform': emailform,
      'email_subscribed': events_user.email_subscribed,
      'noticeform': notices_subscribe_form,
      'notice_subscribed': notice_user.subscribed,
      'notice_subscribed_categories' : main_categories,
  })


@pagelet_login_required
def email_verify(request):
  primary_entry = None
  if request.method == 'POST':
    try:
      if 'primary' in request.POST or 'primary_2' in request.POST:
        entry = UserEmail.objects.get(pk= request.POST['id'])
        authenticated = PasswordCheck.exists_for(user=entry.user,\
            service='email_auth')
        if authenticated:
          if entry.verified:
            request.user.email = entry.email
            request.user.save()
            messages.success(request,"Primary email has been changed.")
          else:
            messages.error(request,"Email need to be verified first.")
        else:
          if 'primary' in request.POST:
            primary_entry = entry

      if 'delete' in request.POST:
        entry = UserEmail.objects.get(pk= request.POST['id'])
        if entry.user==request.user:
          if entry.email== request.user.email:
            messages.error(request,"Primary email address can't be deleted.")
          else:
            messages.success(request, "Email deleted successfuly.")
            entry.delete()
        else:
          messages.error(request, "This email entry can't be deleted.")

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
          send_verification_mail(confirmation_key,entry.email)
          messages.success(request,"A verification link has been sent"+\
            " to your email address.")
        else:
          messages.error(request,"Max limit of verification for this email" +\
              " has been reached for today")
    except Exception as e:
      logger.error(str(e))

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
          send_verification_mail(confirmation_key,email)
          mail_to_primary(email,request.user.email)
          messages.success(request,"A verification link has been sent"+\
              " to your email address.")

  if 'confirm_key' in request.GET:
    confirmation_key = request.GET['confirm_key']
    try:
      email_profile = UserEmail.objects.filter(user=\
          request.user).get(confirmation_key=confirmation_key)
      if email_profile.last_datetime_created + datetime.timedelta(2) < timezone.now():
        messages.error(request,"The verification-key expired.")
      elif UserEmail.objects.filter(email=email_profile.email,
          verified=True).exclude(user=email_profile.user).exists():
        messages.error("This email can not be verified as another user has already"
            " verified it as his/her email address.")
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


def password_reset_request(request):
  if request.method == 'POST':
    form = PasswordResetRequestForm(request.POST)
    if form.is_valid():
      email = form.cleaned_data['email']
      if not User.objects.filter(email=email).exists():
        messages.error(request, "No such email exists.")
      elif not UserEmail.objects.filter(email=email, verified=True).exists():
        messages.error(request, "Password can not be reset as your primary"+\
              " email is not verified. Please verify it first.")
      else:
        user = User.objects.get(email=email)
        salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
        reset_key = hashlib.sha1(salt+email).hexdigest()
        if PasswordReset.objects.filter(user=user).exists():
          entry = PasswordReset.objects.get(user=user)
          if entry.last_datetime_created.date() == datetime.date.today():
            entry.verify_num= entry.verify_num + 1
          else:
            entry.verify_num = 1
          if entry.verify_num < 4 :
            entry.reset_key= reset_key
            entry.last_datetime_created = datetime.datetime.today()
            entry.save()
            send_passwordreset_mail(reset_key,email)
            messages.success(request,"A password reset link has been sent"+\
                " to your email address.")
          else:
            messages.error(request,"Max limit of password reset for this"+\
                " account has been reached for today")
        else:
          new_entry = PasswordReset(user=user, reset_key =reset_key,
              last_datetime_created=datetime.datetime.today(), verify_num=1)
          new_entry.save()
          send_passwordreset_mail(reset_key,email)
          messages.success(request,"A password reset link has been sent"+\
              " to your email address.")
      return HttpResponseRedirect(reverse('close_dialog', kwargs={
            'dialog_name': 'forgot_pass'
      }))
    else:
      messages.error(request, "Invalid email address.")
  form = PasswordResetRequestForm()
  return render(request, 'utilities/dialogs/forgot_password.html',{
      'form':form,
  })


def password_reset(request):
  reset_key = request.GET['reset_key']
  if request.method == 'POST':
    entry = PasswordReset.objects.get(reset_key=reset_key)
    form = PasswordResetForm(request.POST)
    if form.is_valid():
      password1 = request.POST['password1']
      password2 = request.POST['password2']
      if password1 == password2:
        entry.user.set_password(password1)
        entry.user.save()
        messages.success(request,'Password changed successfully')
        entry.delete()
        return HttpResponseRedirect(reverse('close_dialog', kwargs={
              'dialog_name': 'pass_reset'
        }))
      else:
        messages.error(request,'New passwords do not match.')
  else:
    message = ''
    try:
      entry = PasswordReset.objects.get(reset_key=reset_key)
      if entry.last_datetime_created + datetime.timedelta(1) < timezone.now():
        message = "The key expired."
      else:
        form = PasswordResetForm()
        return render(request, 'utilities/dialogs/password_reset.html', {
            'form': form,
        })
    except PasswordReset.DoesNotExist:
      messages.error(request, "Invalid request to reset password.")
      return HttpResponseRedirect(reverse('close_dialog', kwargs={
            'dialog_name': 'pass_reset'
      }))
    return render(request, 'utilities/dialogs/pass_message.html',{
        'message':message,
    })
  form = PasswordResetForm()
  return render(request, 'utilities/dialogs/password_reset.html', {
      'form': form,
  })


@login_required
def person_search(request):
  if request.is_ajax():
    q = request.GET.get('term','')
    persons = Student.objects.filter(Q(user__name__icontains = q)|Q(user__username__icontains = q)).order_by('-user__username')[:10]
    def person_dict(person):
      return {
        'id':person.user.username,
        'label':str(person)+" ("+str(person.branch.code)+")",
        'value':person.user.name
      }
    data = simplejson.dumps(map(person_dict,persons))
  else:
    data = 'fail'
  return HttpResponse(data,'application/json')


