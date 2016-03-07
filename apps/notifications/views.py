import json

from django.http import HttpResponse
from django.db.models import Q

from notifications.models import Notification, UserNotification
from api.utils import ajax_login_required

def notification_dict(usernotification):
  notification = usernotification.notification
  return {
    'id' : usernotification.pk,
    'app' : notification.app,
    'datetime' : notification.datetime_created.strftime('%Y-%m-%d %H:%M:%S'),
    'content' : notification.text,
    'url' : notification.url,
    'viewed': 1 if usernotification.viewed else 0
  }

@ajax_login_required
def fetch(request):
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
      print usernotifications.count()
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

@ajax_login_required
def mark_read(request):
  if request.method == 'POST':
    pk = request.POST['id']
    usernotification = UserNotification.objects.get_or_none(user=request.user, pk=pk)
    if usernotification:
      usernotification.viewed = True
      usernotification.save()
      not_viewed = UserNotification.objects.filter(user=request.user, viewed=False).count()
      data = json.dumps({
        'not_viewed': not_viewed
      })
      return HttpResponse(data, content_type='application/json')

@ajax_login_required
def mark_all_read(request):
  if request.method == 'POST':
    usernotifications = UserNotification.objects.filter(user=request.user, viewed=False)
    for usernotification in usernotifications:
      usernotification.viewed = True
      usernotification.save()
    not_viewed = 0
    data = json.dumps({
      'not_viewed': not_viewed
    })
    return HttpResponse(data, content_type='application/json')
