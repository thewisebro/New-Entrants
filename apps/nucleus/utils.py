import poplib
import smtplib

from django.conf import settings

from nucleus.models import WebmailAccount

def check_pop_login(webmail_username, password):
  """
  Returns None if webmail pop is not working.
  or True/False depending on webmail pop username/password matches or not.
  """
  try:
    try:
      server = poplib.POP3(settings.POP3_HOST)
    except Exception as e:
      return None
    server.user(webmail_username)
    server.pass_(password) # raises an Exception if password is wrong
  except Exception as e:
    return False
  else:
    return True

def check_smtp_login(webmail_username, password):
  """
  Returns None if webmail smtp is not working.
  or True/False depending on webmail smtp username/password matches or not.
  """
  try:
    try:
      server = smtplib.SMTP(settings.EMAIL_HOST)
    except Exception as e:
      return None
    server.login(webmail_username, password) # raises an Exception if password is wrong
  except Exception as e:
    return False
  else:
    return True

def check_webmail_login(webmail_username, password):
  # This function is written such that it is optimistic in time.
  smtp_result = check_smtp_login(webmail_username, password)
  if smtp_result:
    return True
  else:
    pop_result = check_pop_login(webmail_username, password)
    if smtp_result == False:
      return True if pop_result else False
    else:
      return pop_result

def is_user_django_loginable(user, password):
  """
  Returns True if
  either user is active
  or webmail is not working
  or webmail username/password matches.
  """
  if user.is_active:
    return True
  webmail_matched = None
  result = check_webmail_login(user.username, password)
  if not result == None:
    webmail_matched = webmail_matched or result
  if not webmail_matched:
    webmail_accounts = user.webmailaccount_set.all()
    for webmail_account in webmail_accounts:
      result = check_webmail_login(webmail_account.webmail_id, password)
      if not result == None:
        webmail_matched = webmail_matched or result
      if result:
        break
  return bool(webmail_matched)

def get_webmail_account(username):
  """ Returns WebmailAccount instance or None
  """
  webmail_account = WebmailAccount.objects.get_or_none(user__username=username)
  if webmail_account:
    return webmail_account
  return WebmailAccount.objects.get_or_none(webmail_id=username)
