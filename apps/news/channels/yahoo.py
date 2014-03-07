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

def Yahoo(path, category):
  try:
    print "\n\nStarting 'YAHOO NEWS - '"+category+".....\n"
    xml_file = open(path)
    tree = ElementTree.parse(xml_file)
    xml_file.close()
    root = tree.getroot()
    test_var = ""
    source = "Yahoo News"
    image_link = None
    counter = 0

    #os.chdir('media/news_feeds/images')
    for item in root.iter('item'):
      try:
        counter += 1
        title = item.find('title').text
        archive = News.objects.filter(title=title, source=source, channel=category)
        if len(archive) is 0:
          link = item.find('link').text
          des_content = item.find('description').text
          dt = datetime.datetime.now()
          published_date = datetime.datetime(dt.year,dt.month,dt.day)
          image_link = None
          try:
            images = item.findall('{http://search.yahoo.com/mrss/}content')
            image_link = images[0].attrib['url']
          #except Exception as e:
          except:
            pass

          print "\n>>>>>>>>>>>>>>>>>>>>>>       <<<<<<<<<<<<<<<<<<<<<<<<<<<"
          print title
          print "Counter: "+str(counter)

          req = Request(link)
          # Extracting unwanted tags from the item's description
          des = ""
          try:
            des_soup = BeautifulSoup(des_content, convertEntities=BeautifulSoup.HTML_ENTITIES)
            if des_soup is not None:
              des_para = des_soup.find("p")
              if des_para is not None:
                anchor_tag = des_para.find("a")
                if anchor_tag is not None:
                  anchor_tag.extract()
                des = des_para.text
              else:
                des = des_content
          #except Exception as e:
          except:
            pass

          #opener = urllib2.build_opener()
          #opener.addheaders = [('User-agent', 'Mozilla/5.0')]
          html_page = urlopen(req).read()
          soup = BeautifulSoup(html_page, convertEntities=BeautifulSoup.HTML_ENTITIES)
          if html_page is not None:
            news_item = soup.find("div", {"id": "mediaarticlebody"})
            article_text_div = news_item.find("div", {"class": "bd"})
            article_text = article_text_div.findAll("p", recursive = True)
            article_content = ""
            if article_text is not None:
              for paragraph in article_text:
                if not len(paragraph.contents) == 0:
                  article_content +=  str(paragraph) + "\n<br>"  #paragraph.contents[0].encode('utf8')   # converting unicode to a normal string object

            if article_content is not None:
              p = News(item= article_content)
              p.title = title
              p.description_text = smart_str(des)
              p.source = source
              p.channel = category
              p.image_path = "noimage"
              p.article_date = published_date
              p.save()
              if image_link is not None:
                try:
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
  xml_file_path = path + 'yahoo_int.xml'
  Yahoo(xml_file_path, category)

def National(path):
  category = "national"
  xml_file_path = path + 'yahoo_nat.xml'
  Yahoo(xml_file_path, category)

def Sports(path):
  category = "sports"
  xml_file_path = path + 'yahoo_sports.xml'
  Yahoo(xml_file_path, category)

def selectAll(path):
  International(path)
  National(path)
  Sports(path)

####################'End of INDIAN EXPRESS' #####################################################
