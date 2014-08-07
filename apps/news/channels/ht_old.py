#!/usr/bin/python

# Third Party Imports
from xml.etree import ElementTree
from BeautifulSoup import BeautifulSoup, NavigableString

# Python Imports
import urllib2
import re
import subprocess
import os
import HTMLParser
import datetime

# App Imports
from news_feeds.models import news_feeds

################### THE HINDUSTAN TIMES ################################

def ht(path, category):

    xml_file = open(path)
    tree = ElementTree.parse(xml_file)
    xml_file.close()
    root = tree.getroot() # if tree is not null
    test_var = ""
    source = "Hindustan Times"
    counter = 0

    os.chdir('media/news_feeds/images')

    image_path = "noimage"
    for item in root.iter('item'):
      try:
        title = item.find('title').text
        link = item.find('link').text
        des = item.find('description').text
        try:
          des = des.split('<img')
          des = des[0]
        except:
          pass
        #print("here")
        #from dateutil.parser import *
        #from dateutil.tz import *
        #from datetime import *
        dt = datetime.datetime.now()
        published_date = datetime.datetime(dt.year,dt.month,dt.day)
        #print(published_date)
        #a = parse(published_date, ignoretz=True)
        #print(a.strftime() )
        if item.find('enclosure') is not None:
          image_path = item.find('enclosure').attrib['url']

       

        print("\n\nTITLE: "+title)
        print("Image_link: "+image_path)
        print("Des: "+des)
        
         
        opener = urllib2.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]

        html_page = opener.open(link).read()
        soup = BeautifulSoup(html_page)

        news_item_type = 0  # Just to make the code neat.
        if html_page is not None:
          news_item = ""
          """
          if soup.find("div",{"class":"body_txt"}) is not None:
            news_item = soup.find("div",{"class":"body_txt"})
            if news_item is not None:
              news_item_type = 1
          """
          if soup.find("div",{"class":"sty_txt"}) is not None:
            news_item = soup.find("div",{"class":"sty_txt"})
            if news_item is not None:
              news_item_type = 2
          else:
            continue

          article_content = ""
          if news_item_type == 1:
            print("IN - 1")
            article_content = news_item.find("span", {"id":"ctl00_ContentPlaceHolder1_HTStoryPageControl_Para1"}).contents[0].encode('utf8')
            article_content += strip_tags(news_item.find("span", {"id":"ctl00_ContentPlaceHolder1_HTStoryPageControl_Para2"}), ['br']).contents[0].encode('utf8')
            print("check-1")

            article_text = news_item.findAll("p", recursive = True)   # iterative 'p' finding
            invalid_tags = ['a', 'b', 'strong', 'i', 'span', 'u', 'img', 'abbr', 'small', 'select', 'sub', 'sup', 'label', 'big', 'acronym', 'button', 'em', 'del', 'dfn',
                             'input', 'script', 'map', 'q', 'object', 'samp', 'textarea', 'tt', 'var']
            print("check-2")
            if article_text is not None:            
              print("check-3")
              for paragraph in article_text:
                print("In for loop")
                if len(paragraph.contents) != 0:
                  print(paragraph.contents)
                  if paragraph.contents[0]:
                    print("para-1-1")
                    #print(strip_tags(paragraph, invalid_tags))   # converting unicode to a normal string object
                    #print(strip_tags(paragraph, invalid_tags).contents[0].encode('utf8'))
                    #print(strip_tags(paragraph, invalid_tags).text)
                    article_content += strip_tags(paragraph, invalid_tags).text

                    print("para-1-2")
                  else:
                    print("para-1-else")
                else:
                  print("para-2")
              print("check-5")
              print(article_content)
            else:
              print("article_text == None")
              continue          
          elif news_item_type == 2:   # need to be checked.
            print("IN - 2")
            article_text = news_item.findAll("p", recursive = True)   # iterative 'p' finding
            if article_text is not None:
              article_content = ""
              for paragraph in article_text:
                if not len(paragraph.contents) == 0:
                  article_content += paragraph.contents[0].encode('utf8') + "</br>"  # converting unicode to a normal string object
              print(article_content)
            else:
               continue   # To prevent entering the next code with empty 'article_text'.
          else:
            print("news_item_type: "+news_item_type)
            continue

          source = "HINDUSTAN TIMES"
          
          p = news_feeds(item= article_content)
          p.title = title
          p.description_text = des
          if image_path != "noimage":
            try:
              ext = os.path.splitext(image_path)[1]
              unique_image_name = hashlib.sha1(str(source + str(title))).hexdigest()
              image_name =  unique_image_name + ext
              image_link = 'images/'+image_name
              p.image_path = image_link
              p.article_date = published_date
              p.channel = channel
              p.source = source
              p.save()
              wget = 'wget -nc -O %s "%s"' % (image_name, image_path)
              download = subprocess.Popen(wget, shell = True) 
              download.wait()
              print(image_name + " Item Successfully Saved.")
            except:
              pass
          else:
            try:
              p.image_path = image_path
              p.article_date = published_date
              p.channel = channel
              p.source = source
              p.save()
              print("NOIMAGE saved")
            except:
              pass 
          
        image_path = "noimage"  # At end of xml root item for loop.
      except:
        pass

    os.chdir('../../..')
    print("\n\n"+os.getcwd()+"\n")
    return True  
