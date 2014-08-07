import logging
import json as simplejson

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.db.models import Q

from feeds.models import *

logger = logging.getLogger('channel-i_logger')

def feed_dict(feed):
  dictionary = {
    'id' : feed.pk,
    'app' : feed.app,
    'datetime' : feed.last_modified.strftime('%Y-%m-%d %H:%M:%S'),
    'content' : feed.content,
    'link' : feed.link,
  }
  if feed.user:
    dictionary.update({
      'username': feed.user.username,
      'html_name': feed.user.html_name,
    })
  return dictionary

def fetch(request):
  if request.is_ajax() and request.method == 'GET':
#    try:
      action = request.GET['action']
      pk = request.GET['id']
      json = None
      feeds = Feed.objects.all()
      #if not user.is_authenticated or not request.user.in_group('Student'):
        #feeds = feeds.exclude(app__in=['vle','buysell'])
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
      return HttpResponse(json,mimetype='application/json')
#    except Exception as e:
#      logger.exception('Exception accured in feeds/fetch : '+str(e))
#      return HttpResponse('')
