import json as simplejson

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.db.models import Q

from moderation.models import Reportable
from feeds.models import *

def feed_dict(feed):
  dictionary = {
    'id' : feed.pk,
    'app' : feed.app,
    'datetime' : feed.last_modified.strftime('%Y-%m-%d %H:%M:%S'),
    'content' : feed.content,
    'link' : feed.link,
    'reportable': issubclass(feed.instance_type.model_class(), Reportable),
    'content_type_pk': feed.instance_type.pk if feed.instance_type else '',
    'object_pk': feed.instance.pk if feed.instance else '',
  }
  if feed.user:
    dictionary.update({
      'username': feed.user.username,
      'html_name': feed.user.html_name,
    })
  return dictionary

def fetch(request):
  action = request.GET['action']
  pk = request.GET['id']
  json = None
  feeds = Feed.objects.filter(shown_feed=None)
  if not request.user.is_authenticated() or not request.user.in_group('Student'):
    feeds = feeds.exclude(app__in=['buysell'])
  if not action == 'previous':
    number = int(request.GET['number'])
    if action == 'first':
      pass
    elif action == 'next':
      feeds = feeds.filter(pk__lt = pk)
    json = simplejson.dumps({'feeds':map(feed_dict,feeds[:number]),'more':int(feeds.count()>number)})
  else:
    feeds = feeds.filter(pk__gt = pk)
    json = simplejson.dumps({'feeds':map(feed_dict,feeds)})
  return HttpResponse(json, content_type='application/json')
