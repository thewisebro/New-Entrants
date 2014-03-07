#from xml.etree import ElementTree
#from BeautifulSoup import BeautifulSoup, NavigableString
#import urllib2
#import re
#import subprocess
import os
#import HTMLParser

from  django.shortcuts import render_to_response

#from settings import MEDIA_URL
#import hashlib
#import datetime
#import uuid
from models import News
from channels import hindu, ie, msn, toi, yahoo, bbc #, nyt

#from similarity import compare
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext

from haystack.query import SearchQuerySet

def home(request):
   #print dir(hindu)
   q = request.GET.get('q')
   models = request.GET.get('models')
   if q is not None and models is not None:
    var = '/news/search/?q='+q+"&models="+models
    return HttpResponseRedirect(var)
   else:
    news = News.objects.all().order_by('-article_date') #exclude(image_path = "noimage")
    items = news.values_list('pk','title','image_path','description_text','article_date','source')
    return render_to_response('news/home.html', {'items':items}, context_instance = RequestContext(request))

def national(request):
   q = request.GET.get('q')
   models = request.GET.get('models')
   if q is not None and models is not None:
    var = '/news/search/?q='+q+"&models="+models
    return HttpResponseRedirect(var)
   else:
    news = News.objects.filter(channel = "national").order_by('-article_date')
    items = news.values_list('pk','title','image_path','description_text','article_date','source')
    return render_to_response('news/home.html', {'items':items}, context_instance = RequestContext(request))

def international(request):
   q = request.GET.get('q')
   models = request.GET.get('models')
   if q is not None and models is not None:
    var = '/news/search/?q='+q+"&models="+models
    return HttpResponseRedirect(var)
   else:
    news = News.objects.filter(channel = "international").order_by('-article_date')
    items = news.values_list('pk','title','image_path','description_text','article_date','source')
    return render_to_response('news/home.html', {'items':items}, context_instance = RequestContext(request))

def sports(request):
   q = request.GET.get('q')
   models = request.GET.get('models')
   if q is not None and models is not None:
    var = '/news/search/?q='+q+"&models="+models
    return HttpResponseRedirect(var)
   else:
    news = News.objects.filter(channel = "sports").order_by('-article_date')
    items = news.values_list('pk','title','image_path','description_text','article_date','source')
    return render_to_response('news/home.html', {'items':items}, context_instance = RequestContext(request))

def entertainment(request):
   q = request.GET.get('q')
   models = request.GET.get('models')
   if q is not None and models is not None:
    var = '/news/search/?q='+q+"&models="+models
    return HttpResponseRedirect(var)
   else:
    news = News.objects.filter(channel = "entertainment").order_by('-article_date')
    items = news.values_list('pk','title','image_path','description_text','article_date','source')
    return render_to_response('news/home.html', {'items':items}, context_instance = RequestContext(request))


def news_item(request, item_id):
    news = News.objects.get(pk = item_id)
    pk = news.pk
    title = news.title
    image = news.image_path
    source = news.source
    article_date = news.article_date
    content = news.item  #.encode('utf8')
    #print(title+", "+content)

    #related = "hello"
    related = SearchQuerySet().more_like_this(news)[:5]

    item = {
      'pk':pk,
      'title':title,
      'image':image,
      'source':source,
      'article_date':article_date,
      'content':content,
      'related':related,
    }

    return render_to_response('news/news_item.html', item, context_instance=RequestContext(request))

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


