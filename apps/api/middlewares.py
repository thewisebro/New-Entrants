import json

from django.http import Http404, StreamingHttpResponse, HttpResponse,\
                        HttpResponseRedirect
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.conf import settings
from django.contrib.auth.views import redirect_to_login
from django.contrib.auth import REDIRECT_FIELD_NAME

from nucleus.models import User


class SiteMiddleware(object):
  def process_view(self, request, view_func, view_args, view_kwargs):
    # If site is internet, user should be logged in
    if settings.SITE_ID == 2 and not request.path.startswith(
        settings.LOGIN_URL) and not request.user.is_authenticated():
      return redirect_to_login(request.path, settings.LOGIN_URL,
          REDIRECT_FIELD_NAME)
    return None

class DelegateMiddleware(object):
  def process_view(self, request, view_func, view_args, view_kwargs):
    #Below line is for jukebox
    request.jb_user = request.user
    #Below line is for all rest api views
    request.rest_user = request.user

    if request.user.is_authenticated():
      account_username = view_kwargs.pop('account_username', None)
      if account_username is None:
        request.owner = request.user.owner()
      else:
        account = User.objects.get_or_none(username=account_username)
        if account and request.user.accounts.filter(username=account.username).exists():
          request.owner = request.user.owner(account)
          request.user = request.owner.account
          request.account_username = account_username
        else:
          raise Http404
    return None

class AjaxMessaging(object):
  def process_response(self, request, response):
    if request.is_ajax():
      try:
        if response['Content-Type'] in ["application/javascript", "application/json"]:
          try:
            if isinstance(response, StreamingHttpResponse):
              return response
            content = json.loads(response.content)
          except ValueError:
            return response
          django_messages = []

          for message in messages.get_messages(request):
            django_messages.append({
              "level": message.level,
              "message": message.message,
              "extra_tags": message.tags,
            })

          if isinstance(content, dict):
            content['ajax_messages'] = django_messages
            content['is_user_authenticated'] = request.user.is_authenticated()
            content['user_username'] = request.user.username

          response.content = json.dumps(content)
      except Exception as e:
        pass
    return response
