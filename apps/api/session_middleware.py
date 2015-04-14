import base64
import pickle

from nucleus.models import User
from django.contrib.sessions.models import Session

class SessionUserMiddleware(object):
  def process_request(self, request):
    try:
      session = Session.objects.get(pk=request.session._session_key)
      encoded_data = base64.decodestring(session.session_data)
      _hash, pickled = encoded_data.split(':', 1)
      if 'username' in pickled:
        username = pickled.split('username')[1][7:].split('U')[0][:-2]
        try:
          request.user = User.objects.get(username=username)
        except User.DoesNotExist:
          username = pickled.split('username')[1][5:].split('U')[0]
          request.user = User.objects.get(username=username)
      request.jb_user = request.user
    except Exception as e:
      pass
    return None

