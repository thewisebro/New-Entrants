#!/usr/bin/python

# Third Party Imports
from BeautifulSoup import BeautifulSoup, NavigableString

# Python Imports
from xml.etree import ElementTree
from urllib2 import Request, urlopen, URLError
from dateutil import parser
import re
import subprocess
import os
#import urllib2
import datetime

#Django Imports
from django.utils.encoding import smart_str

# App Imports
from news.models import *

######################## 'TIMES OF INDIA' ####################################

def Toi(path, channel):
  try:
    print "\n\nStarting 'TIMES OF INDIA - '"+channel+".....\n"
    xml_file = open(path)
    tree = ElementTree.parse(xml_file)
    xml_file.close()
    root = tree.getroot()
    test_var = ""
    #source = "Times Of India"
    counter = 0
    source = Source.objects.get(name='Times Of India')

    #print(os.getcwd())
    #os.chdir('media/news_feeds/images')
    for item in root.iter('item'):
      counter += 1
      try:
        title = item.find('title').text
        channel = Channel.objects.get(name=channel)
        archive = News.objects.filter(title=title, source=source, channel=channel)
        if len(archive) is 0:
          link = item.find('link').text
          des_content = item.find('description').text
          pub_date_string = item.findtext('pubDate')
          published_date = parser.parse(pub_date_string)

          des_soup = BeautifulSoup(des_content, convertEntities=BeautifulSoup.HTML_ENTITIES)
          des = des_soup.contents[0]
          if des.startswith( '<img ' ):
            des = ''

          print "\n>>>>>>>>>>>>>>>>>>>>>>       <<<<<<<<<<<<<<<<<<<<<<<<<<<"
          print title
          print "Counter: "+str(counter)
          print des

          req = Request(link)
          html_page = ""
          html_page = urlopen(req).read()
          soup = BeautifulSoup(html_page, convertEntities=BeautifulSoup.HTML_ENTITIES)
          if html_page is not None:
             news_item = soup.find("div",{"class":"Normal"})

             if news_item is not None:
              """
              if news_item.find("script"):
                article_text_raw = news_item.findAll("script")
                for scrap in article_text_raw:
                  scrap.extract()
              """
              article_text = news_item.findAll(text = True)
              article_content = ""
              if len(article_text) is not 0:
                for text in article_text:
                  if text is not None:
                    #print(text.encode('utf8'))
                    article_content += str(text) + "\n<br>"  #text.encode('utf8')   # converting unicode to a normal string object
              else:
                continue

              p = News(item= article_content)
              p.title = title
              print des
              p.description_text = smart_str(des)
              p.source = source
              p.channel = channel
              p.image_path = "noimage"
              p.article_date = published_date
              p.save()
              image_div = soup.find("div",{"class": "mainimg1"})
              if image_div is not None:
                image = image_div.find("img")
                if image is not None:
                  try:
                    image_link = image.get("src")
                    ext = os.path.splitext(image_link)[1]
                    print ext
                    if "?" in ext:
                      ext = ext.split('?')[0]
                    ext = ext.lower()
                    if ext is None or ext is '':
                      ext = '.jpg'
                    unique_image_name = str(p.pk)
                    image_name =  unique_image_name + ext
                    image_path = "images/" + image_name
                    p.image_path = image_path
                    p.save()
                    wget = 'wget -U firefox -nc -O %s "%s"' % (image_name, image_link)
                    download = subprocess.Popen(wget, shell = True)
                    download.wait()
                  except Exception as e:
                    print e
                    pass
                  #except Exception as e: print "Exception accured while downloading :",e,"      wget '"+image_link+"'"
                  print "Saved_with_image"
                else:
                  print "No Image Found!!"
              else:
                print "Saved_Without_image "
                continue
        else:
          print "Already saved!!"
          print "Counter: "+ str(counter)
      except Exception as e:
        print e
        pass
  except Exception as e:
    print e
    pass

def International(path):
  channel = "International"
  xml_file_path = path + 'toi_int.xml'
  Toi(xml_file_path, channel)

def National(path):
  channel = "National"
  xml_file_path = path + 'toi_nat.xml'
  Toi(xml_file_path, channel)

def Sports(path):
  channel = "Sports"
  xml_file_path = path + 'toi_sports.xml'
  Toi(xml_file_path, channel)

def Entertainment(path):
  channel = "Entertainment"
  xml_file_path = path + 'toi_entertainment.xml'
  Toi(xml_file_path, channel)

#def Science(path):
#  channel = "Technology"

def Technology(path):
  channel = "Technology"
  xml_file_path = path + 'toi_tech.xml'
  Toi(xml_file_path, channel)
  xml_file_path = path + 'toi_science.xml'
  Toi(xml_file_path, channel)

def Education(path):
  channel = "Education"
  xml_file_path = path + 'toi_education.xml'
  Toi(xml_file_path, channel)

def Health(path):
  channel = "Health"
  xml_file_path = path + 'toi_health.xml'
  Toi(xml_file_path, channel)

def selectAll(path):
  International(path)
  National(path)
  Sports(path)
  Entertainment(path)
  #Science(path)
  Technology(path)
  Education(path)
  Health(path)


