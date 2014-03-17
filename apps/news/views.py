#from xml.etree import ElementTree
#from BeautifulSoup import BeautifulSoup, NavigableString
#import urllib2
#import re
#import subprocess
import os
#import HTMLParser

from  django.shortcuts import HttpResponse, render_to_response

#from settings import MEDIA_URL
#import hashlib
#import datetime
#import uuid

import json as simplejson
from models import News
from channels import hindu, ie, msn, toi, yahoo, bbc #, nyt

#from similarity import compare
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
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
    "channel": item.channel,
    "source": item.source
  }

def home(request):
   #print dir(hindu)
   q = request.GET.get('q')
   models = request.GET.get('models')
   if q is not None and models is not None:
    var = '/news/search/?q='+q+"&models="+models
    return HttpResponseRedirect(var)
   else:
    marker = 1
    news = News.objects.all().order_by('-article_date')
    json = simplejson.dumps({'news':map(lambda x:prepare_content(x), news), 'marker': marker})
    return HttpResponse(json,content_type='application/json')

def fetch_more_news(request):
  try:
    #channel = request.POST.get('channel')
    arg = request.POST.get('arg')
    marker = request.POST.get('marker')
    marker = int(marker)
    feed_limit = 20
    #feed_limit = 50 if category is 'News' else 20
    if arg in NC.CATEGORIES:
      print arg
      channel = arg.lower()
      if channel is 'news':
        news = News.objects.all().order_by('-article_date')[(marker*feed_limit) : ((marker+1)*feed_limit)]
      else:
        news = News.objects.filter(channel = channel).order_by('-article_date')[(marker*feed_limit) : ((marker+1)*feed_limit)]
   #TODO: elif arg in NC.SOURCES:
    else:
      print arg
      source = arg.lower()
      news = News.objects.filter(source = source).order_by('-article_date')[(marker*feed_limit) : ((marker+1)*feed_limit)]
    json = simplejson.dumps({'news':map(lambda x:prepare_content(x), news), 'marker': marker+1})
    return HttpResponse(json,content_type='application/json')
  except Exception as e:
    print e
    return HttpResponse("Invalid Request!");

def categories_list(request):
  cat_list = NC.CATEGORIES
  json = simplejson.dumps({'categories': cat_list});
  return HttpResponse(json,content_type='application/json')

def get_by_source(request):
  source = request.POST.get('source');
  print source
  marker = 1
  news = News.objects.filter(source = source).order_by('-article_date')[:20]
  json = simplejson.dumps({'news':map(lambda x:prepare_content(x), news), 'marker': marker})
  return HttpResponse(json,content_type='application/json')

def national(request):
   q = request.GET.get('q')
   models = request.GET.get('models')
   if q is not None and models is not None:
    var = '/news/search/?q='+q+"&models="+models
    return HttpResponseRedirect(var)
   else:
    marker = 1
    news = News.objects.filter(channel = "national").order_by('-article_date')[:20]
    json = simplejson.dumps({'news':map(lambda x:prepare_content(x), news), 'marker': marker})
    return HttpResponse(json,content_type='application/json')

def international(request):
   q = request.GET.get('q')
   models = request.GET.get('models')
   if q is not None and models is not None:
    var = '/news/search/?q='+q+"&models="+models
    return HttpResponseRedirect(var)
   else:
    marker = 1
    news = News.objects.filter(channel = "international").order_by('-article_date')[:20]
    json = simplejson.dumps({'news':map(lambda x:prepare_content(x), news), 'marker': marker})
    return HttpResponse(json,content_type='application/json')

def sports(request):
   q = request.GET.get('q')
   models = request.GET.get('models')
   if q is not None and models is not None:
    var = '/news/search/?q='+q+"&models="+models
    return HttpResponseRedirect(var)
   else:
    marker = 1
    news = News.objects.filter(channel = "sports").order_by('-article_date')[:20]
    json = simplejson.dumps({'news':map(lambda x:prepare_content(x), news), 'marker': marker})
    return HttpResponse(json,content_type='application/json')

def entertainment(request):
   q = request.GET.get('q')
   models = request.GET.get('models')
   if q is not None and models is not None:
    var = '/news/search/?q='+q+"&models="+models
    return HttpResponseRedirect(var)
   else:
    marker = 1
    news = News.objects.filter(channel = "entertainment").order_by('-article_date')[:20]
    json = simplejson.dumps({'news':map(lambda x:prepare_content(x), news), 'marker': marker})
    return HttpResponse(json,content_type='application/json')

def technology(request):
   q = request.GET.get('q')
   models = request.GET.get('models')
   if q is not None and models is not None:
    var = '/news/search/?q='+q+"&models="+models
    return HttpResponseRedirect(var)
   else:
    marker = 1
    news = News.objects.filter(channel = "technology").order_by('-article_date')[:20]
    json = simplejson.dumps({'news':map(lambda x:prepare_content(x), news), 'marker': marker})
    return HttpResponse(json,content_type='application/json')

def education(request):
   q = request.GET.get('q')
   models = request.GET.get('models')
   if q is not None and models is not None:
    var = '/news/search/?q='+q+"&models="+models
    return HttpResponseRedirect(var)
   else:
    marker = 1
    news = News.objects.filter(channel = "education").order_by('-article_date')[:20]
    json = simplejson.dumps({'news':map(lambda x:prepare_content(x), news), 'marker': marker})
    return HttpResponse(json,content_type='application/json')

def health(request):
   q = request.GET.get('q')
   models = request.GET.get('models')
   if q is not None and models is not None:
    var = '/news/search/?q='+q+"&models="+models
    return HttpResponseRedirect(var)
   else:
    marker = 1
    news = News.objects.filter(channel = "health").order_by('-article_date')[:20]
    json = simplejson.dumps({'news':map(lambda x:prepare_content(x), news), 'marker': marker})
    return HttpResponse(json,content_type='application/json')

def news_item(request, item_id):
    news = News.objects.get(pk = item_id)
    pk = news.pk
    title = news.title
    image = news.image_path
    channel = news.channel
    source = news.source
    article_date = news.article_date
    content = news.item  #.encode('utf8')

    related = SearchQuerySet().more_like_this(news)
    formatted_datetime = article_date.strftime("%A, %d. %B %Y %I:%M%p");

    item = {
      'pk': str(pk),
      'title': title,
      'image': image,
      'channel': channel,
      'source': source,
      'article_date': formatted_datetime,
      'content': content,
      #'related': related,
    }

    json = simplejson.dumps({'item': item})
    return HttpResponse(json,content_type='application/json')

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
  os.chdir('media/news/images')
  print(os.getcwd())
  try:
    #ht(path, 'national')
    #ht(path, 'sports')

    hindu.Sports(path)
    toi.Sports(path)
    ie.Sports(path)
    msn.Sports(path)
    yahoo.Sports(path)
    bbc.Sports(path)

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


