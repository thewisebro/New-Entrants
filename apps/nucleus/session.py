import json
from datetime import datetime

from django.contrib.sessions.backends.cached_db import SessionStore as DbStore
from django.contrib.sessions.models import Session
from django.utils.encoding import force_unicode

from nucleus.models import PHPSession, User

def get_php_session_data(session_data):
  return {}

class SessionStore(DbStore):
    def __init__(self, session_key=None):
        super(SessionStore, self).__init__(session_key)

    def save(self, must_create=False):
        super(SessionStore, self).save(must_create=must_create)
        php_s = PHPSession()
        php_s.session_key = self.session_key
        session_data = self._session
        expire_date = self.get_expiry_date()
        user_id = session_data.get('_auth_user_id', None)
        user = User.objects.get_or_none(pk=user_id)
        if user:
            php_s.username = user.username
        if expire_date:
            php_s.expire_date = expire_date
        php_s.session_data = json.dumps(get_php_session_data(session_data))
        php_s.datetime_created = datetime.now()
        php_s.save()

    def delete(self, session_key=None):
        super(SessionStore, self).delete(session_key=session_key)
        if session_key is None:
            session_key = self.session_key
        try:
            PHPSession.objects.get(session_key=session_key).delete()
        except PHPSession.DoesNotExist:
            pass
