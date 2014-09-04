import json

from django.http import HttpResponse
from django.db.models import Q

from notifications.models import Notification, UserNotification


def notification_dict(usernotification):
  notification = usernotification.notification
  return {
    'id' : notification.pk,
    'app' : notification.app,
    'datetime' : notification.datetime_created.strftime('%Y-%m-%d %H:%M:%S'),
    'content' : notification.text,
    'url' : notification.url,
    'viewed': 1 if usernotification.viewed else 0
  }


def fetch(request):
  data = json.dumps({})
  if request.is_ajax() and request.method == 'GET' and\
                          request.user.is_authenticated():
    usernotifications = request.user.usernotification_set.all()
    not_viewed = usernotifications.filter(viewed=False).count()
    action = request.GET['action']
    pk = request.GET['id']
    if not action == 'previous':
      number = int(request.GET['number'])
      if action == 'first':
        pass
      elif action == 'next':
        usernotifications = usernotifications.filter(pk__lt=pk)
      data = json.dumps({
          'notifications': map(notification_dict,
            usernotifications[:number]),
          'more': int(usernotifications.count() > number),
          'not_viewed': not_viewed,
      })
    else:
      usernotifications = usernotifications.filter(pk__gt=pk)
      data = json.dumps({
          'notifications': map(notification_dict, usernotifications),
          'not_viewed': not_viewed,
      })
  return HttpResponse(data, content_type='application/json')
