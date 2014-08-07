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

def Bbc(path, channel):
  try:
    print "\n\nStarting 'BBC NEWS - '"+channel+".....\n"
    xml_file = open(path)
    tree = ElementTree.parse(xml_file)
    xml_file.close()
    root = tree.getroot()
    test_var = ""
    #source = "BBC News"
    image_link = None
    counter = 0
    source = Source.objects.get(name='BBC News')
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
          des = item.find('description').text
          dt = datetime.datetime.now()
          published_date = datetime.datetime(dt.year,dt.month,dt.day)
          try:
            images = item.findall('{http://search.yahoo.com/mrss/}thumbnail')
            image_link = images[1].attrib['url']
          except:
            pass
          #except Exception as e:
            #pass

          # Extracting unwanted tags from the item's description
          """
          des_soup = BeautifulSoup(des_content)
          image = des_soup.find("img")
          image.extract()
          des = str(des_soup.text)
          """

          print "\n>>>>>>>>>>>>>>>>>>>>>>       <<<<<<<<<<<<<<<<<<<<<<<<<<<"
          print title
          print "Counter: "+str(counter)

          req = Request(link)
          html_page = ""
          html_page = urlopen(req).read()
          soup = BeautifulSoup(html_page, convertEntities=BeautifulSoup.HTML_ENTITIES)
          if html_page is not None:
            news_item = soup.find("div", {"class": "story-body"})
            """
            if news_item is not None:
              article_text_raw = news_item.findAll("script")
              for scrap in article_text_raw:
                scrap.extract()
            """
            if news_item is not None:
              article_text = news_item.findAll("p", recursive = True)
              article_content = ""
              if article_text is not None:
                for paragraph in article_text:
                  if not len(paragraph.contents) == 0:
                    article_content +=  str(paragraph) + "\n<br>"  #paragraph.contents[0].encode('utf8')   # converting unicode to a normal string object

              if article_content is not None:
                #if image_link is None:
                #image_link = "noimage"
                p = News(item= article_content)
                p.title = title
                p.description_text = smart_str(des)
                p.source = source
                p.channel = channel
                p.image_path = "noimage"
                p.article_date = published_date
                p.save()
                if image_link is not None:
                  try:
                    #image_link = image.get("src")
                    ext = os.path.splitext(image_link)[1]
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
                  #except Exception as e:
                  except:
                    pass
                    #print e
                  #except Exception as e: print "Exception accured while downloading :",e,"      wget '"+image_link+"'"
                  print "Saved_with_image"
                else:
                  print "Saved_Without_image "+str(p.pk)
                  continue
        else:
          print "\n Already There...."
      except:
        pass
  #except Exception as e:
  except:
    pass
    #print e


def International(path):
  channel = "International"
  xml_file_path = path + 'bbc_int.xml'
  Bbc(xml_file_path, channel)

def National(path):
  channel = "National"
  xml_file_path = path + 'bbc_nat.xml'
  Bbc(xml_file_path, channel)

def Sports(path):
  channel = "Sports"
  xml_file_path = path + 'bbc_sports.xml'
  Bbc(xml_file_path, channel)

def Entertainment(path):
  channel = "Entertainment"
  xml_file_path = path + 'bbc_entertainment.xml'
  Bbc(xml_file_path, channel)

def Technology(path):
  channel = "Technology"
  xml_file_path = path + 'bbc_science.xml'
  Bbc(xml_file_path, channel)

def Tech(path):
  channel = "Technology"
  xml_file_path = path + 'bbc_tech.xml'
  Bbc(xml_file_path, channel)

def Health(path):
  channel = "Health"
  xml_file_path = path + 'bbc_html.xml'
  Bbc(xml_file_path, channel)

def selectAll(path):
  International(path)
  National(path)
  Sports(path)
  Entertainment(path)
  Technology(path)
  Tech(path)
  Health(path)


##################################  'End of BBC NEWS' ##########################

