from datetime import datetime

from django.contrib.sessions.backends.db import SessionStore as DbStore
from django.contrib.sessions.models import Session
from django.utils.encoding import force_unicode

from nucleus.models import PHPSession, User

class SessionStore(DbStore):
    def __init__(self, session_key=None):
        super(SessionStore, self).__init__(session_key)

    def save(self, must_create=False):
        super(SessionStore, self).save(must_create=must_create)
        # TODO:
        # need to work more on this function, extend the django
        # functionality to php_session too. It's working for now.
        php_s = PHPSession()
        php_s.session_key = self._session_key
        session_data, expire_date = self.get_session_data()
        user_id = session_data.get('_auth_user_id', None)
        user = User.objects.get_or_none(pk=user_id)
        if user:
            php_s.username = user.username
        if expire_date:
            php_s.expire_date = expire_date
        php_s.datetime_created = datetime.today()
        print self._session_key
        php_s.save()

    def delete(self, session_key=None):
        super(SessionStore, self).delete(session_key=session_key)
        if session_key is None:
            session_key = self.session_key
        try:
            PHPSession.objects.get(session_key=session_key).delete()
        except PHPSession.DoesNotExist:
            pass

    def get_session_data(self):
        try:
            s = Session.objects.get(session_key=self.session_key)
            return self.decode(force_unicode(s.session_data)), s.expire_date
        except:
            return {}
