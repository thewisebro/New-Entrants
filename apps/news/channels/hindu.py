#!/usr/bin/python

# Third Party Imports
from BeautifulSoup import BeautifulSoup, NavigableString

# Python Imports
from xml.etree import ElementTree
from urllib2 import Request, urlopen, URLError
import re
import subprocess
import os
import datetime

#Django Imports
from django.utils.encoding import smart_str

# App Imports
from news.models import *

################### For THE HINDU:  #####################################

def Hindu(path, channel):
  try:
    print "\n\nStarting 'THE HINDU - '"+channel+".....\n"
    xml_file = open(path)
    tree = ElementTree.parse(xml_file)
    xml_file.close()
    root = tree.getroot()
    test_var = ""
    #source = "THE HINDU"
    counter = 0
    source = Source.objects.get(name='The Hindu')

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
          pub_date = item.find('pubDate')
          print "PUB DATE = "
          print list(pub_date)
          dt = datetime.datetime.now()
          published_date = datetime.datetime(dt.year,dt.month,dt.day)
          print "\n>>>>>>>>>>>>>>>>>>>>>>       <<<<<<<<<<<<<<<<<<<<<<<<<<<"
          print title
          print "Counter: "+str(counter)

          req = Request(link)
          html_page = urlopen(req).read()
          soup = BeautifulSoup(html_page, convertEntities=BeautifulSoup.HTML_ENTITIES)
          #opener = urllib2.build_opener()
          #opener.addheaders = [('User-agent', 'Mozilla/5.0')]
          #html_page = opener.open(link).read()
          #soup = BeautifulSoup(html_page, convertEntities=BeautifulSoup.HTML_ENTITIES)

          if html_page is not None:
           news_item = soup.find("div", {"id":"left-column"})
           if news_item is not None:
            article_text_div = news_item.find("div",{"class":"article-text"})
            if article_text_div is not None:
              #article_text_raw = article_text_div.findAll("script")
              article_text = article_text_div.findAll("p")   # iterative 'p' finding
              article_content = ""
              if article_text is not None:
                for paragraph in article_text:
                  if not len(paragraph.contents) == 0:
                    article_content += str(paragraph) + "\n<br>"
                    #article_content += paragraph.contents[0] #.encode('utf8')   # converting unicode toa normal string object

              if article_content is not None:
                p = News(item = article_content)
                p.title = title
                p.description_text = smart_str(des)
                image_link = "noimage"
                p.source = source
                p.channel = channel
                p.image_path = image_link
                p.article_date = published_date
                p.save()
                #print "p.pk= "+ str(p.pk)

                # Single Image Item
                multiple_pics = news_item.findAll("div",{"class":"pic"})
                #print multiple_pics
                if len(multiple_pics) == 0:
                  image = news_item.find("img",{"class":"main-image"})
                  if image is not None:
                    image_link = image.get('src')
                    # Single image
                    try:
                      ext = os.path.splitext(image_link)[1]
                      if "?" in ext:
                        ext = ext.split('?')[0]
                      ext = ext.lower()
                      if ext is None or ext is '':
                        ext = '.jpg'
                      #unique_image_name = hashlib.sha1(str(source) + str(title)).hexdigest()
                      unique_image_name = str(p.pk)
                      #unique_image_name = str(uuid.uuid1()).replace('-','_')
                      image_name =  unique_image_name + ext
                      image_path = "images/" + image_name
                      p.image_path = image_path
                      p.save()
                      wget = 'wget -U firefox -nc -O %s "%s"' % (image_name, image_link)
                      download = subprocess.Popen(wget, shell = True)
                      download.wait()
                      print("Saved_with_image")
                    except:
                      pass
                  else:
                    print "Saved Without Image"

                    #except Exception as e: print "Exception accured while downloading :",e,"      wget '"+image_link+"'"
                else:
                  incrementor = 1
                  for image_div in multiple_pics:
                    img = image_div.find("img")
                    img_link = img.get('src')
                    try:
                      ext = os.path.splitext(img_link)[1]
                      if "?" in ext:
                        ext = ext.split('?')[0]
                      ext = ext.lower()
                      if ext is None or ext is '':
                        ext = '.jpg'
                      unique_image_name = str(p.pk)+"-"+str(incrementor)
                      image_name =  unique_image_name + ext
                      image_path = "images/" + image_name
                      p.image_path = image_path
                      p.save()
                      wget = 'wget -nc -O %s "%s"' % (image_name, img_link)
                      download = subprocess.Popen(wget, shell = True)
                      download.wait()
                      incrementor += 1
                    except:
                      pass
                    #except Exception as e: print "Exception accured while downloading :",e,"      wget '"+img_link+"'"
                  print("Saved_with_imageset")
        else:
          print "\n Already There..."
      except Exception as e:
        print e
        pass
  #except Exception as e:
  except Exception as e:
    print e
    pass


def International(path):
  channel = "International"
  xml_file_path = path + 'hindu_int.xml'
  Hindu(xml_file_path, channel)

def National(path):
  channel = "National"
  xml_file_path = path + 'hindu_nat.xml'
  Hindu(xml_file_path, channel)

def Sports(path):
  channel = "Sports"
  xml_file_path = path + 'hindu_sports.xml'
  Hindu(xml_file_path, channel)

def Entertainment(path):
  channel = "Entertainment"
  xml_file_path = path + 'hindu_entertainment.xml'
  Hindu(xml_file_path, channel)

def Technology(path):
  channel = "Technology"
  xml_file_path = path + 'hindu_science_tech.xml'
  Hindu(xml_file_path, channel)

def Education(path):
  channel = "Education"
  xml_file_path = path + 'hindu_education.xml'
  Hindu(xml_file_path, channel)

def Health(path):
  channel = "Health"
  xml_file_path = path + 'hindu_health.xml'
  Hindu(xml_file_path, channel)

def selectAll(path):
  International(path)
  National(path)
  Sports(path)
  Entertainment(path)
  Technology(path)
  Education(path)
  Health(path)

######################## END OF 'THE HINDU' ##################################
