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

######################## 'TIMES OF INDIA' ####################################

def Toi(path, category):
  try:
    print "\n\nStarting 'TIMES OF INDIA - '"+category+".....\n"
    xml_file = open(path)
    tree = ElementTree.parse(xml_file)
    xml_file.close()
    root = tree.getroot()
    test_var = ""
    source = "Times Of India"
    counter = 0

    #print(os.getcwd())
    #os.chdir('media/news_feeds/images')
    for item in root.iter('item'):
      counter += 1
      try:
        title = item.find('title').text
        archive = News.objects.filter(title=title, source=source, channel=category)
        if len(archive) is 0:
          link = item.find('link').text
          des_content = item.find('description').text
          dt = datetime.datetime.now()
          published_date = datetime.datetime(dt.year,dt.month,dt.day)

          des_soup = BeautifulSoup(des_content, convertEntities=BeautifulSoup.HTML_ENTITIES)
          des = des_soup.contents[0]

          print "\n>>>>>>>>>>>>>>>>>>>>>>       <<<<<<<<<<<<<<<<<<<<<<<<<<<"
          print title
          print "Counter: "+str(counter)
          print des
          print "cp"

          req = Request(link)
          html_page = ""
          html_page = urlopen(req).read()
          soup = BeautifulSoup(html_page, convertEntities=BeautifulSoup.HTML_ENTITIES)
          print "cp-1"
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
                print "cp-2"
                for text in article_text:
                  if text is not None:
                    #print(text.encode('utf8'))
                    article_content += str(text) + "\n<br>"  #text.encode('utf8')   # converting unicode to a normal string object
              else:
                continue

              p = News(item= article_content)
              p.title = title
              p.description_text = smart_str(des)
              p.source = source
              p.channel = category
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
                    unique_image_name = str(p.pk)
                    image_name =  unique_image_name + ext
                    image_path = "images/" + image_name
                    p.image_path = image_path
                    p.save()
                    wget = 'wget -nc -O %s "%s"' % (image_name, image_link)
                    download = subprocess.Popen(wget, shell = True)
                    download.wait()
                  except Exception as e:
                    print e
                    pass
                  #except Exception as e: print "Exception accured while downloading :",e,"      wget '"+image_link+"'"
                  print "Saved_with_image"
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
  category = "international"
  xml_file_path = path + 'toi_int.xml'
  Toi(xml_file_path, category)

def National(path):
  category = "national"
  xml_file_path = path + 'toi_nat.xml'
  Toi(xml_file_path, category)

def Sports(path):
  category = "sports"
  xml_file_path = path + 'toi_sports.xml'
  Toi(xml_file_path, category)

def Entertainment(path):
  category = "entertainment"
  xml_file_path = path + 'toi_entertainment.xml'
  Toi(xml_file_path, category)

def Science(path):
  category = "science-tech"
  xml_file_path = path + 'toi_science.xml'
  Toi(xml_file_path, category)

def Tech(path):
  category = "science-tech"
  xml_file_path = path + 'toi_tech.xml'
  Toi(xml_file_path, category)

def Education(path):
  category = "education"
  xml_file_path = path + 'toi_education.xml'
  Toi(xml_file_path, category)

def Health(path):
  category = "health"
  xml_file_path = path + 'toi_health.xml'
  Toi(xml_file_path, category)

def selectAll(path):
  International(path)
  National(path)
  Sports(path)
  Entertainment(path)
  Science(path)
  Tech(path)
  Education(path)
  Health(path)


