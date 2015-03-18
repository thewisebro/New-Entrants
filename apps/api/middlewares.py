import json

from django.http import Http404, StreamingHttpResponse
from django.contrib import messages

from nucleus.models import User

class DelegateMiddleware(object):
  def process_view(self, request, view_func, view_args, view_kwargs):
    #Below line is for jukebox
    request.jb_user = request.user

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
    return response
