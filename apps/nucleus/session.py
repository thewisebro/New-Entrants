import json

from datetime import datetime, timedelta

from django.contrib.sessions.backends.cached_db import SessionStore as DbStore

from nucleus.models import PHPSession, User
import redis
redis_client = redis.Redis("localhost")

def get_php_session_data(session_data):
  return {}

class SessionStore(DbStore):
    def __init__(self, session_key=None):
        super(SessionStore, self).__init__(session_key)

    def save(self, must_create=False):
        super(SessionStore, self).save(must_create=must_create)
        php_s = PHPSession()
        redis_data = dict()
        php_s.session_key = self.session_key
        session_data = self._session
        expire_date = self.get_expiry_date()
        user_id = session_data.get('_auth_user_id', None)
        redis_data["user_id"] = user_id
        user = User.objects.get_or_none(pk=user_id)
        if user:
            php_s.username = user.username
            redis_data["username"] = user.username
        if expire_date:
            php_s.expire_date = expire_date
            if user:
              cr_date = (datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
              ex_date = expire_date.strftime("%Y-%m-%d %H:%M:%S")
              timediff = (datetime.strptime(ex_date, "%Y-%m-%d %H:%M:%S") - datetime.strptime(cr_date, "%Y-%m-%d %H:%M:%S")).total_seconds()
              json_payload = json.dumps(redis_data)  # Verbose_name: "s_data" -> "session_data"
              redis_client.set("session:"+self.session_key, json_payload)
              redis_client.expire("session:"+self.session_key, int(timediff))
        php_s.session_data = json.dumps(get_php_session_data(session_data))
        php_s.datetime_created = datetime.now()
        php_s.save()

    def delete(self, session_key=None):
        super(SessionStore, self).delete(session_key=session_key)
        if session_key is None:
            session_key = self.session_key
        try:
            PHPSession.objects.get(session_key=session_key).delete()
            redis_client.delete("session:"+session_key)
        except PHPSession.DoesNotExist:
            pass
