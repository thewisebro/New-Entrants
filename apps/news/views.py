#from xml.etree import ElementTree
#from BeautifulSoup import BeautifulSoup, NavigableString
#import urllib2
#import re
#import subprocess
import os
#import HTMLParser

from  django.shortcuts import HttpResponse, render_to_response
from django.core.urlresolvers import reverse
#from settings import MEDIA_URL
#import hashlib
#import datetime
#import uuid

import json as simplejson
from models import *
from channels import hindu, ie, msn, toi, yahoo, bbc #, nyt

#from similarity import compare
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.conf import settings
from django.contrib import messages

from news import constants as NC
from haystack.query import SearchQuerySet

def prepare_content(item):
  formatted_datetime = item.article_date.strftime("%A, %d. %B %Y %I:%M%p");
  return {
    "pk": str(item.pk),
    "title": item.title,
    "image": item.image_path,
    "description_text": item.description_text,
    "article_date": formatted_datetime,
    "channel": item.channel.name,
    "source": item.source.name
  }


def store_default_pref(newsuser, channel):
    channel_pref = ChannelPref(channel=channel, newsuser=newsuser)
    channel_pref.save()

def search(request):
  print request.GET.get('q')
  sqs = SearchQuerySet().autocomplete(content_auto=request.GET.get('q'))[:5]
  #suggestions = map(lambda result: related_item_dict(News.objects.get_or_none(pk = result.pk)), sqs)
  print "SEARCH"
  #print suggestions
  suggestions = map(lambda result:{'title':result.title,'id':result.pk}, sqs)
  json = simplejson.dumps({
    'suggestions': suggestions
  })
  print json
  return HttpResponse(json, content_type='application/json')

def home(request):
   q = request.GET.get('q')
   models = request.GET.get('models')
   if q is not None and models is not None:
    var = '/news/search/?q='+q+"&models="+models
    return HttpResponseRedirect(var)
   else:
    newsuser = NewsUser.objects.get_or_none(user=request.user)
    if newsuser is None:
      print "newuser is None"
      newsuser = NewsUser(user=request.user)
      newsuser.save()
      map(lambda c: (store_default_pref(newsuser, c)), Channel.objects.all())
    marker = 1
    news = News.objects.all().order_by('-article_date')[:50]
    json = simplejson.dumps({'news':map(lambda x:prepare_content(x), news), 'marker': marker})
    return HttpResponse(json, content_type='application/json')

def fetch_more_news(request):
  try:
    newsuser = NewsUser.objects.get_or_none(user=request.user)
    if newsuser is None:
      return HttpResponse(simplejson.dumps({'msg': 'NOUSER'}), content_type='application/json')
    #channel = request.POST.get('channel')
    arg = request.POST.get('arg')
    marker = request.POST.get('marker')
    marker = int(marker)
    feed_limit = NC.FEED_LIMIT
    #feed_limit = 50 if category is 'News' else 20
    if arg == 'News':
      news = News.objects.all().order_by('-article_date')[(marker*feed_limit) : ((marker+1)*feed_limit)]
    #TODO:  Remove NC.CATEGORIES AND ADD CHECK FROM DB
    elif arg in NC.CATEGORIES:
      channel = Channel.objects.get(name=arg)
      news = News.objects.filter(channel = channel).order_by('-article_date')[(marker*feed_limit) : ((marker+1)*feed_limit)]
    #TODO: elif arg in NC.SOURCES:
    else:
      source = Source.objects.get(name=arg)
      news = News.objects.filter(source = source).order_by('-article_date')[(marker*feed_limit) : ((marker+1)*feed_limit)]
    json = simplejson.dumps({'news':map(lambda x:prepare_content(x), news), 'marker': marker+1})
    return HttpResponse(json,content_type='application/json')
  except Exception as e:
    print e
    return HttpResponse("Invalid Request!");

def channels_list(request):
  try:
    newsuser = NewsUser.objects.get_or_none(user=request.user)
    if newsuser is None:
      return HttpResponse(simplejson.dumps({'msg': 'NOUSER'}), content_type='application/json')
    channels = Channel.objects.all()
    json = simplejson.dumps({'channels':map(lambda x:x.name, channels)})
    #cat_list = NC.CATEGORIES
    return HttpResponse(json,content_type='application/json')
  except Exception as e:
    return HttpResponse(e)

def fetch_channel_prefs(request):
  try:
    newsuser = NewsUser.objects.get_or_none(user=request.user)
    if newsuser is None:
      return HttpResponse(simplejson.dumps({'msg': 'NOUSER'}), content_type='application/json')
    prefs = ChannelPref.objects.filter(newsuser=newsuser)
    json = simplejson.dumps({'c_prefs': map(lambda p: {'channel': p.channel.name, 'value': p.pref_value}, prefs)})
    print json
    return HttpResponse(json,content_type='application/json')
  except:
    messages.error(request, 'Error has occured!')
    return HttpResponse(simplejson.dumps({'msg': 'FAILURE'}), content_type='application/json')

def update_channel_prefs(request):
  try:
    newsuser = NewsUser.objects.get_or_none(user=request.user)
    if newsuser is None:
      return HttpResponse(simplejson.dumps({'msg': 'NOUSER'}), content_type='application/json')
    pref_value = request.POST.get('value')
    print pref_value
    channel_name = (request.POST.get('element_id')).replace('pref_', '')
    channel = Channel.objects.get(name=channel_name)
    channel_pref = ChannelPref.objects.get(newsuser=newsuser, channel=channel)
    channel_pref.pref_value = pref_value
    channel_pref.save()
    messages.success(request, 'Preferences Updated')
    return HttpResponse(simplejson.dumps({'msg': 'SUCCESS'}), content_type='application/json')
  except:
    messages.error(request, 'Error has occured!')
    return HttpResponse(simplejson.dumps({'msg': 'FAILURE'}), content_type='application/json')


def get_by_source(request):
  try:
    newsuser = NewsUser.objects.get_or_none(user=request.user)
    if newsuser is None:
      return HttpResponse(simplejson.dumps({'msg': 'NOUSER'}), content_type='application/json')
    source = request.POST.get('source');
    print source
    marker = 1
    source = Source.objects.get(name=source)
    news = News.objects.filter(source = source).order_by('-article_date')[:20]
    json = simplejson.dumps({'news':map(lambda x:prepare_content(x), news), 'marker': marker})
    return HttpResponse(json,content_type='application/json')
  except:
    return HttpResponse("Invalid Request!")

def national(request):
  try:
    newsuser = NewsUser.objects.get_or_none(user=request.user)
    if newsuser is None:
      return HttpResponse(simplejson.dumps({'msg': 'NOUSER'}), content_type='application/json')
    q = request.GET.get('q')
    models = request.GET.get('models')
    if q is not None and models is not None:
      var = '/news/search/?q='+q+"&models="+models
      return HttpResponseRedirect(var)
    else:
      marker = 1
      channel = Channel.objects.get(name='National')
      news = News.objects.filter(channel = channel).order_by('-article_date')[:20]
      json = simplejson.dumps({'news':map(lambda x:prepare_content(x), news), 'marker': marker})
      return HttpResponse(json,content_type='application/json')
  except Exception as e:
    return HttpResponse(e)

def international(request):
  try:
    newsuser = NewsUser.objects.get_or_none(user=request.user)
    if newsuser is None:
      return HttpResponse(simplejson.dumps({'msg': 'NOUSER'}), content_type='application/json')
    q = request.GET.get('q')
    models = request.GET.get('models')
    if q is not None and models is not None:
      var = '/news/search/?q='+q+"&models="+models
      return HttpResponseRedirect(var)
    else:
      marker = 1
      channel = Channel.objects.get(name='International')
      news = News.objects.filter(channel = channel).order_by('-article_date')[:20]
      json = simplejson.dumps({'news':map(lambda x:prepare_content(x), news), 'marker': marker})
      return HttpResponse(json,content_type='application/json')
  except:
    return HttpResponse("Invalid Request!")

def sports(request):
  try:
    newsuser = NewsUser.objects.get_or_none(user=request.user)
    if newsuser is None:
      return HttpResponse(simplejson.dumps({'msg': 'NOUSER'}), content_type='application/json')
    q = request.GET.get('q')
    models = request.GET.get('models')
    if q is not None and models is not None:
      var = '/news/search/?q='+q+"&models="+models
      return HttpResponseRedirect(var)
    else:
      marker = 1
      channel = Channel.objects.get(name='Sports')
      news = News.objects.filter(channel = channel).order_by('-article_date')[:20]
      json = simplejson.dumps({'news':map(lambda x:prepare_content(x), news), 'marker': marker})
      return HttpResponse(json,content_type='application/json')
  except:
    return HttpResponse("Invalid Request!")

def entertainment(request):
  try:
    newsuser = NewsUser.objects.get_or_none(user=request.user)
    if newsuser is None:
      return HttpResponse(simplejson.dumps({'msg': 'NOUSER'}), content_type='application/json')
    q = request.GET.get('q')
    models = request.GET.get('models')
    if q is not None and models is not None:
      var = '/news/search/?q='+q+"&models="+models
      return HttpResponseRedirect(var)
    else:
      marker = 1
      channel = Channel.objects.get(name='Entertainment')
      news = News.objects.filter(channel = channel).order_by('-article_date')[:20]
      json = simplejson.dumps({'news':map(lambda x:prepare_content(x), news), 'marker': marker})
      return HttpResponse(json,content_type='application/json')
  except:
    return HttpResponse("Invalid Request!")

def technology(request):
  try:
    newsuser = NewsUser.objects.get_or_none(user=request.user)
    if newsuser is None:
      return HttpResponse(simplejson.dumps({'msg': 'NOUSER'}), content_type='application/json')
    q = request.GET.get('q')
    models = request.GET.get('models')
    if q is not None and models is not None:
      var = '/news/search/?q='+q+"&models="+models
      return HttpResponseRedirect(var)
    else:
      marker = 1
      channel = Channel.objects.get(name='Technology')
      news = News.objects.filter(channel = channel).order_by('-article_date')[:20]
      json = simplejson.dumps({'news':map(lambda x:prepare_content(x), news), 'marker': marker})
      return HttpResponse(json,content_type='application/json')
  except:
    return HttpResponse("Invalid Request!")

def education(request):
  try:
    newsuser = NewsUser.objects.get_or_none(user=request.user)
    if newsuser is None:
      return HttpResponse(simplejson.dumps({'msg': 'NOUSER'}), content_type='application/json')
    q = request.GET.get('q')
    models = request.GET.get('models')
    if q is not None and models is not None:
      var = '/news/search/?q='+q+"&models="+models
      return HttpResponseRedirect(var)
    else:
      marker = 1
      channel = Channel.objects.get(name='Education')
      news = News.objects.filter(channel = channel).order_by('-article_date')[:20]
      json = simplejson.dumps({'news':map(lambda x:prepare_content(x), news), 'marker': marker})
      return HttpResponse(json,content_type='application/json')
  except:
    return HttpResponse("Invalid Request!")

def health(request):
  try:
    newsuser = NewsUser.objects.get_or_none(user=request.user)
    if newsuser is None:
      return HttpResponse(simplejson.dumps({'msg': 'NOUSER'}), content_type='application/json')
    q = request.GET.get('q')
    models = request.GET.get('models')
    if q is not None and models is not None:
      var = '/news/search/?q='+q+"&models="+models
      return HttpResponseRedirect(var)
    else:
      marker = 1
      channel = Channel.objects.get(name='Health')
      news = News.objects.filter(channel = channel).order_by('-article_date')[:20]
      json = simplejson.dumps({'news':map(lambda x:prepare_content(x), news), 'marker': marker})
      return HttpResponse(json,content_type='application/json')
  except:
    return HttpResponse("Invalid Request!")

def item_dict(news_item):
  formatted_datetime = news_item.article_date.strftime("%A, %d. %B %Y %I:%M%p")
  item = {
    'pk': str(news_item.pk),
    'title': news_item.title,
    'image': news_item.image_path,
    'channel': news_item.channel.name,
    'source': news_item.source.name,
    'article_date': formatted_datetime,
    'content': news_item.item,
  }
  return item

def related_item_dict(news_item):
  formatted_datetime = news_item.article_date.strftime("%A, %d. %B %Y %I:%M%p")
  item = {
    'pk': str(news_item.pk),
    'title': news_item.title,
    'description_text': news_item.description_text,
    'image': news_item.image_path,
    'channel': news_item.channel.name,
    'source': news_item.source.name,
    'article_date': formatted_datetime,
  }
  return item

def news_item(request, item_id):
  try:
    newsuser = NewsUser.objects.get_or_none(user=request.user)
    if newsuser is None:
      return HttpResponse(simplejson.dumps({'msg': 'NOUSER'}), content_type='application/json')
    news_item = News.objects.get(pk = item_id)
    main = item_dict(news_item)
    #print main
    """
    pk = news.pk
    title = news.title
    image = news.image_path
    channel = news.channel
    source = news.source
    article_date = news.article_date
    content = news.item  #.encode('utf8')
    """
    more_like_this = SearchQuerySet().more_like_this(news_item)[:3]
    if more_like_this is not None:
      related = map(lambda result: related_item_dict(News.objects.get_or_none(pk = result.pk)), more_like_this)
      json = simplejson.dumps({'main':main, 'related':related})
      return HttpResponse(json,content_type='application/json')
    else:
      print main
      json = simplejson.dumps({'main':main, 'related':[]})
      return HttpResponse(json,content_type='application/json')

    """
    item = {
      'pk': str(pk),
      'title': title,
      'image': image,
      'channel': channel.name,
      'source': source.name,
      'article_date': formatted_datetime,
      'content': content,
      'related': related
    }
    json = simplejson.dumps({'item': item})
    return HttpResponse(json,content_type='application/json')
    """
  except Exception as e:
    return HttpResponse(e)


'''
def related_news(item_1, item_2):
    try:
      news_item_1 = news_feeds.objects.get(pk=item_1)
      news_item_2 = news_feeds.objects.get(pk=item_2)
      related_news = related_news.objects.create()
      if compare(item_1.item, item_2.item) > 0.2:
         news_item_1.related_news_set.add(news_item_2)  '''

'''def visible(element):
  if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
    return False
  #elif re.match('<!--.*-->', str(element)):i
    #return False
  #elif re.match('/*.**/', str(element)):
   return False
  return True
'''


def html_data_extracter(request):
  path = os.path.dirname(__file__)
  path = os.path.join(path, 'xml_files/')
  print(path)
  print(os.getcwd())
  os.chdir(settings.NEWS_IMAGES_ROOT)
  print(os.getcwd())
  try:
    #ht(path, 'national')
    #ht(path, 'sports')

    """
    hindu.Entertainment(path)
    toi.Entertainment(path)
    ie.Entertainment(path)
    msn.Entertainment(path)
    bbc.Entertainment(path)
    """
    hindu.Technology(path)
    toi.Technology(path)
    ie.Technology(path)
    bbc.Technology(path)
    hindu.Education(path)
    toi.Education(path)
    ie.Education(path)
    hindu.Health(path)
    toi.Health(path)
    ie.Health(path)
    bbc.Health(path)

    return HttpResponse("Task Completed!!")
  except Exception as e:
    return HttpResponse(e)


"""
  try:
    ie_nat(path)
    print("ie")
  except Exception as e:return HttpResponse("AT IE"+e)

  try:
    hindu_nat(path)
    print("hindu")
  except:
    pass
  print("MAIN-1")

  #print("MAIN-2")
  try:
    toi_nat(path)
    print("3-1")
  except:
    pass
"""

#def get_channel(channel):


  #print("In main 'for loop'")
  #return HttpResponse("Task completed!! " + os.getcwd()+"</br> "+test_var)

      #else:
        # return HttpResponse("Invalid link !!")      # to 404 page here


def strip_tags(soup, invalid_tags):
   #soup = BeautifulSoup(html)
   for tag in soup.findAll(True):
     if tag.name in invalid_tags:
       s = ""
       for c in tag.contents:
        if not isinstance(c, NavigableString):
          c = strip_tags(unicode(c), invalid_tags)
        s += unicode(c)
       tag.replaceWith(s)
   return soup


'''def get_data(request):
  from news_feeds.models import news_feeds
  from django.shortcuts import render_to_response

  for item in news_models.objects.get(pk=)'''


