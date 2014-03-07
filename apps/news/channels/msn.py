#!/usr/bin/python

# Third Party Imports
from BeautifulSoup import BeautifulSoup, NavigableString

# Python Imports
from xml.etree import ElementTree
from urllib2 import Request, urlopen, URLError
import re
import subprocess
import os
#import urllib2
import datetime

#Django Imports
from django.utils.encoding import smart_str

# App Imports
from news.models import News

#############################  'INDIAN EXPRESS' ################################

def Msn(path, category):
  try:
    print "\n\nStarting 'MSN NEWS - '"+category+".....\n"
    xml_file = open(path)
    tree = ElementTree.parse(xml_file)
    xml_file.close()
    root = tree.getroot()
    test_var = ""
    source = "MSN NEWS"
    counter = 0

    #os.chdir('media/news_feeds/images')
    for item in root.iter('item'):
      try:
        counter += 1
        title = item.find('title').text
        archive = News.objects.filter(title=title, source=source, channel=category)
        if len(archive) is 0:
          link = item.find('link').text
          des = item.find('description').text
          dt = datetime.datetime.now()
          published_date = datetime.datetime(dt.year,dt.month,dt.day)

          print "\n>>>>>>>>>>>>>>>>>>>>>>       <<<<<<<<<<<<<<<<<<<<<<<<<<<"
          print title
          print "Counter: "+str(counter)

          req = Request(link)
          html_page = ""
          html_page = urlopen(req).read()
          soup = BeautifulSoup(html_page, convertEntities=BeautifulSoup.HTML_ENTITIES)
          if html_page is not None:
            news_item = soup.find("div", {"id": "page1"})
            image_div = news_item.find("div", {"class": "img"})
            if image_div is not None:
              image = image_div.find("img")
              image_div.extract()

            if news_item is not None:
              article_text = news_item.findAll("p", recursive = True)   # iterative 'p' finding
              article_content = ""
              if article_text is not None:
                for paragraph in article_text:
                  if not len(paragraph.contents) == 0:
                    article_content +=  str(paragraph) + "\n<br>"  #paragraph.contents[0].encode('utf8')   # converting unicode to a normal string object

              if article_content is not None:
                image_link = "noimage"
                p = News(item= article_content)
                p.title = title
                p.description_text = smart_str(des)
                p.source = source
                p.channel = category
                p.image_path = image_link
                p.article_date = published_date
                p.save()
                #image_div = news_item.find("div",{"class": "story-image"})
                #image = image_div.find("img")
                if image is not None:
                  try:
                    image_link = image.get("src")
                    ext = os.path.splitext(image_link)[1]
                    unique_image_name = str(p.pk)
                    image_name =  unique_image_name + ext
                    image_path = "images/" + image_name
                    p.image_path = image_path
                    p.save()
                    wget = 'wget -nc -O %s "%s"' % (image_name, image_link)
                    download = subprocess.Popen(wget, shell = True)
                    download.wait()
                  except:
                    pass
                  #except Exception as e: print "Exception accured while downloading :",e,"      wget '"+image_link+"'"
                  print "Saved_with_image"
                else:
                  print "Saved_Without_image "+str(p.pk)
                  continue
      except:
        pass
  #except Exception as e:
  except:
    pass


def International(path):
  category = "international"
  xml_file_path = path + 'msn_int.xml'
  Msn(xml_file_path, category)

def National(path):
  category = "national"
  xml_file_path = path + 'msn_nat.xml'
  Msn(xml_file_path, category)

def Sports(path):
  category = "sports"
  xml_file_path = path + 'msn_sports.xml'
  Msn(xml_file_path, category)

def Entertainment(path):
  category = "entertainment"
  xml_file_path = path + 'msn_entertainment.xml'
  Msn(xml_file_path, category)

def selectAll(path):
  International(path)
  National(path)
  Sports(path)
  Entertainment(path)

##################################  'End of INDIAN EXPRESS' #####################################################
