import json as simplejson

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.db.models import Q
from django.core.cache import cache

from moderation.models import Reportable
from feeds.models import *

def feed_dict(feed):
  dictionary = {
    'id' : feed.pk,
    'app' : feed.app,
    'datetime' : feed.datetime_created.strftime('%Y-%m-%d %H:%M:%S'),
    'content' : feed.content,
    'link' : feed.link,
    'reportable': issubclass(feed.instance_type.model_class(), Reportable),
    'content_type_pk': feed.instance_type.pk if feed.instance_type else '',
    'object_pk': feed.instance_id if feed.instance_id else '',
  }
  if feed.user:
    dictionary.update({
      'username': feed.user.username,
      'user_photo': feed.user.photo_url,
      'html_name': feed.user.html_name,
    })
  return dictionary

def fetch(request):
  action = request.GET['action']
  pk = request.GET['id']
  json = None
  feeds = Feed.objects.filter(shown_feed=None)
  cache_key = 'feeds_student'
  save_json = False
  if not request.user.is_authenticated() or not request.user.in_group('Student'):
    feeds = feeds.exclude(app__in=['buysell'])
    cache_key = 'feeds_nonstudent'
  if not action == 'previous':
    number = int(request.GET['number'])
    if action == 'first':
      try:
        json = cache.get(cache_key)
        if not json:
          save_json = True
      except Exception as e:
        pass
    elif action == 'next':
      feeds = feeds.filter(pk__lt = pk)
    if not json:
      json = simplejson.dumps({'feeds':map(feed_dict,feeds[:number]),'more':int(feeds.count()>number)})
  else:
    feeds = feeds.filter(pk__gt = pk)
    json = simplejson.dumps({'feeds':map(feed_dict,feeds)})
  if save_json:
    try:
      cache.set(cache_key, json)
    except Exception as e:
      pass
  return HttpResponse(json, content_type='application/json')
