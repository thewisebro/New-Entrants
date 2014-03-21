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
from news.models import *

#############################  'INDIAN EXPRESS' ################################

def Ie(path, channel):
  try:
    print "\n\nStarting 'INDIAN EXPRESS - '"+channel+".....\n"
    xml_file = open(path)
    tree = ElementTree.parse(xml_file)
    xml_file.close()
    root = tree.getroot()
    test_var = ""
    #source = "INDIAN EXPRESS"
    counter = 0
    source = Source.objects.get(name='Indian Express')

    #print(os.getcwd())
    #os.chdir('media/news_feeds/images')
    for item in root.iter('item'):
      try:
        counter += 1
        title = item.find('title').text
        channel = Channel.objects.get(name=channel)
        archive = News.objects.filter(title=title, source=source, channel=channel)
        if len(archive) is 0:
          link = item.find('link').text
          des_content = item.find('description').text
          dt = datetime.datetime.now()
          published_date = datetime.datetime(dt.year,dt.month,dt.day)

          # Extracting unwanted tags from the item's description
          des_soup = BeautifulSoup(des_content)
          image = des_soup.find("img")
          image.extract()

          """
            Django's 'smart_str' function in the  django.utils.encoding module, converts a Unicode string to a bytestring using a default encoding of UTF-8  unlike default 'ASCII' encoding
          """
          des = smart_str(des_soup.text)
          print "\n>>>>>>>>>>>>>>>>>>>>>>       <<<<<<<<<<<<<<<<<<<<<<<<<<<"
          print title
          print "Counter: "+str(counter)
          print des

          req = Request(link)
          #opener = urllib2.build_opener()
          #opener.addheaders = [('User-agent', 'Mozilla/5.0')]
          html_page = ""
          html_page = urlopen(req).read()
          soup = BeautifulSoup(html_page, convertEntities=BeautifulSoup.HTML_ENTITIES)
          if html_page is not None:
            news_item = soup.find("div", {"class": "inner-container"})
            """
            if news_item is not None:
              article_text_raw = news_item.findAll("script")
              for scrap in article_text_raw:
                scrap.extract()
            """
            if news_item is not None:
              article_text_div = news_item.find("div", {"class": "section-stories"})
              article_text = article_text_div.findAll("p", recursive = True)   # iterative 'p' finding
              article_content = ""
              if article_text is not None:
                for paragraph in article_text:
                  if not len(paragraph.contents) == 0:
                    article_content +=  str(paragraph) + "\n<br>"  #paragraph.contents[0].encode('utf8')   # converting unicode to a normal string object

              if article_content is not None:
                p = News(item= article_content)
                p.title = title
                p.description_text = des
                p.source = source
                p.channel = channel
                p.image_path = "noimage"
                p.article_date = published_date
                p.save()

                image_div = None
                try:
                  image_div = news_item.find("div",{"class": "story-image"})
                except:
                  pass

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
                    except:
                      pass
                  #except Exception as e: print "Exception accured while downloading :",e,"      wget '"+image_link+"'"
                    print "Saved_with_image"
                else:
                  print "Saved_Without_image "
                  continue
        else:
          print "\nAlready stored!"
          print archive
          print "Counter: "+ str(counter)
      except Exception as e:
        print "\n"+title
        print link
        print "Counter: "+ str(counter)
        print e
        pass
  except Exception as e:
    pass


def International(path):
  channel = "International"
  xml_file_path = path + 'ie_int.xml'
  Ie(xml_file_path, channel)

def National(path):
  channel = "National"
  xml_file_path = path + 'ie_nat.xml'
  Ie(xml_file_path, channel)

def Sports(path):
  channel = "Sports"
  xml_file_path = path + 'ie_sports.xml'
  Ie(xml_file_path, channel)

def Entertainment(path):
  channel = "Entertainment"
  xml_file_path = path + 'ie_entertainment.xml'
  Ie(xml_file_path, channel)

def Technology(path):
  channel = "Technology"
  xml_file_path = path + 'ie_science_tech.xml'
  Ie(xml_file_path, channel)

def Education(path):
  c = "Education"
  xml_file_path = path + 'ie_education.xml'
  Ie(xml_file_path, channel)

def Health(path):
  channel = "Health"
  xml_file_path = path + 'ie_health.xml'
  Ie(xml_file_path, channel)

def selectAll(path):
  International(path)
  National(path)
  Sports(path)
  Entertainment(path)
  Technology(path)
  Education(path)
  Health(path)

##################################  'End of INDIAN EXPRESS' #####################################################

