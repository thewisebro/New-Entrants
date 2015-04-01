from django.core.servers.basehttp import FileWrapper
from django.http import HttpResponse
from django.conf import settings

import os
import mimetypes

from  nucleus.models import User

STATIC_PATH = settings.STATIC_PATH

def photo(request, username=None):
  filepath = ''
  user = None
  if username:
    if username.lower() == 'img':
      filepath = STATIC_PATH + 'images/nucleus/img.png'
    else:
      user = User.objects.get_or_none(username=username)
  elif request.user.is_authenticated():
    user = request.user
  if user and user.photo:
    filepath = user.photo.path
  if not filepath or not os.path.exists(filepath):
    if user and user.in_group('Student Group'):
      filepath = STATIC_PATH + 'images/nucleus/default_group_dp.png'
    else:
      filepath = STATIC_PATH + 'images/nucleus/default_dp.png'
  wrapper = FileWrapper(file(filepath))
  response = HttpResponse(wrapper, content_type=mimetypes.guess_type(filepath)[0])
  response['Content-Length'] = os.path.getsize(filepath)
  response['Cache-Control'] = 'no-cache'
  return response
