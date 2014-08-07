#!/usr/bin/python

# Third Party Imports
from BeautifulSoup import BeautifulSoup, NavigableString

# Python Imports
from xml.etree import ElementTree
import urllib2
import re
import subprocess
import os
import HTMLParser
import datetime

# App Imports
from news.models import News

################### For THE HINDU:  #####################################

def Ht(path, category):
  try:
    xml_file = open(path)
    tree = ElementTree.parse(xml_file)
    xml_file.close()
    root = tree.getroot()
    test_var = ""
    source = "HINDUSTAN TIMES"
    counter = 1

    #print(os.getcwd())
    os.chdir('media/news_feeds/images')

    for item in root.iter('item'):
      title = item.find('title').text
      #archive = news_feeds.objects.filter(title=title, source=source, channel=category)
      print "start extraction..."
      #if len(archive) is 0:
      link = item.find('link').text
      des = item.find('description').text
      dt = datetime.datetime.now()
      published_date = datetime.datetime(dt.year,dt.month,dt.day)
      print ">>>>>>>>>>>>>>>>>>>>>>       <<<<<<<<<<<<<<<<<<<<<<<<<<<"
      print title
      print published_date
      print "Counter: "+str(counter)

      opener = urllib2.build_opener()
      opener.addheaders = [('User-agent', 'Mozilla/5.0')]
      html_page = opener.open(link).read()
      soup = BeautifulSoup(html_page, convertEntities=BeautifulSoup.HTML_ENTITIES)
      print "before souping the page...!!!"
      #print html_page
      if html_page is not None:
        print "yoyo"
        news_item = soup.find("div", {"class": "sty_txt"})
        if news_item is not None:
          print "cp-1"
          #article_text_raw = article_text_div.findAll("script")
          article_text = news_item.findAll("p")   # iterative 'p' finding
          article_content = ""
          if article_text is not None:
            for paragraph in article_text:
              if not len(paragraph.contents) == 0:
                article_content += str(paragraph) + "\n<br>"

          if article_content is not None:
            print "cp-2"
            image_link = "noimage"
            p = news_feeds(item = article_content)
            p.title = title
            p.description_text = des    #html_parser.unescape(des)
            p.source = source
            p.channel = category
            p.image_path = image_link
            p.article_date = published_date
            p.save()
            counter += 1
            print "junction...!!!"
            image_div = news_item.find("div",{"class": "gallery_photo"})

            if image_div is not None:
              image = image_div.find("img")
              print image
              if image is not None:
                try:
                  image_link = image.get("src")
                  print image_link
                  ext = os.path.splitext(image_link)[1]
                  unique_image_name = str(p.pk)
                  image_name =  unique_image_name + ext
                  image_path = "images/" + image_name
                  p.image_path = image_path
                  p.save()
                  wget = 'wget -nc -O %s "%s"' % (image_name, image_link)
                  download = subprocess.Popen(wget, shell = True)
                  download.wait()
                  print "Saved_with_image"
                #except:
                  #pass
                except Exception as e: print "Exception accured while downloading :",e,"      wget '"+image_link+"'"
            else:
              print "Saved_Without_image "+str(p.pk)
              continue

  except Exception as e:
    pass


def International(path):
  category = "international"
  xml_file_path = path + 'ht_int.xml'
  Ht(xml_file_path, category)

def National(path):
  category = "national"
  xml_file_path = path + 'ht_nat.xml'
  Ht(xml_file_path, category)

def Sports(path):
  category = "sports"
  xml_file_path = path + 'ht_sports.xml'
  Ht(xml_file_path, category)

def Entertainment(path):
  category = "entertainment"
  xml_file_path = path + 'ht_entertainment.xml'
  Ht(xml_file_path, category)

#
