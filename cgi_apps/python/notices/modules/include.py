#!/usr/bin/python
import re
import os
import cgi
import subprocess
from constant import *
from datetime import datetime
from BeautifulSoup import BeautifulSoup

current_year = str(datetime.today().year)
curr_year = datetime.today().year

PeopleProxyUrl = "http://people.iitr.ernet.in/Notices/"

def replace(original,content,tempinput):
	tempinput=re.subn(original,content,tempinput)
	return tempinput[0]
				
def safeStripfordb(text):
    return text.replace("'","''").replace("\\","\\\\")

def safeStrip(text):
    text = re.subn(r"&(?!#[0-f]{1,4};)","&amp;",text)[0]
    return text.replace("'","''").replace("\\","\\\\").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")


def ampEscape(text):
    text = re.subn(r"&(?!#[0-f]{1,4};)","&amp;",text)[0]
    return text

def Html2unicode(text):
    text = re.subn("&lt;","<",text)[0]
    text = re.subn("&gt;",">",text)[0]
    text = re.subn("&amp;","&",text)[0]
    text = re.subn("&#([0-f]{4,4});",r"\\u\1",text)[0]
    text = re.subn("'",r"\\'",text)[0]
    return eval("u'"+text+"'")


CatSubcat={}
for cat in Categories:
    category=eval(cat)
    category_order=eval(cat+"_order")
    CatSubcat[cat]=category_order

def correct_urls(html):
  html=pdftoimg(html)
  soup = BeautifulSoup(html)
  links = soup('a')
  for link in links:
    if link.has_key('href'):
      link['href'] = link['href'].replace(' ','%20')
  images = soup('img')    
  for image in images:
    if image.has_key('src'):
      image['src'] = image['src'].replace(' ','%20')
  imgs = soup('img')
  for img in imgs:
    if img.has_key('style'):
      css_properties = img['style'].split(';')
      new_css_properties = []
      for css_property in css_properties:
        splits = css_property.split(':')
        if not (len(splits) == 2 and (splits[0].replace(' ','') == 'min-height' or splits[0].replace(' ','') == 'height')):
          new_css_properties.append(css_property)
      img['style'] = ';'.join(new_css_properties)
    img['style'] = (img['style']+';' if img.has_key('style') else '') + 'max-width:940px;height:auto'
  return str(soup)

def replaceWithContents(element,imglocation):
  ix= element.parent.contents.index(element)
  for child in reversed(element.contents):
    showimage = element.prettify()+"<img src=\""+PeopleProxyUrl+"userfiles/pdfimages/"+imglocation+".png\" width='900px' height='auto'>"
    element.parent.insert(ix,BeautifulSoup(showimage))
    element.extract()

def pdftoimg(html):
  #find ".pdf" in a string
  match = re.compile('\.(pdf)')
  
  # parse page content
  soup = BeautifulSoup(html)

  # check links
  for link in soup.findAll('a'):
    try:
      link['href'] = link['href'].replace('%20',' ')
      href = link['href']
      if re.search(match, href):
        filename = os.path.splitext(os.path.basename(href))[0]
	location = re.split(PeopleProxyUrl,href)[1]
	cmd = ['convert','-append','-density','300','-resize','1024x','-trim', location,'-quality','100','-sharpen','0x1.0','userfiles/pdfimages/'+filename+'.png']
	subprocess.Popen(cmd)
	replaceWithContents(link,filename)
    except Exception,e:
      print e
      pass
  return str(soup)

def pdftoimg2(html):
  #find ".pdf" in a string
  match = re.compile('\.(pdf)')
  
  # parse page content
  soup = BeautifulSoup(html)

  # check links
  for link in soup.findAll('a'):
    try:
      link['href'] = link['href'].replace('%20',' ')
      print link
      href = link['href']
      if re.search(match, href):
        filename = os.path.splitext(os.path.basename(href))[0]
	location = re.split(PeopleProxyUrl,href)[1]
	cmd = ['convert','-append','-density','300','-resize','1024x','-trim', location,'-quality','100','-sharpen','0x1.0','userfiles/pdfimages/'+filename+'.png']
	#subprocess.Popen(cmd)
	replaceWithContents(link,filename)
    except Exception,e:
      print e
      pass
  return str(soup)

def remove_pdfimages(html):
  soup = BeautifulSoup(html)
  images = soup('img')
  starting = PeopleProxyUrl+"userfiles/pdfimages/"
  for image in images:
    if image.has_key('src') and image['src'][:len(starting)] == starting:
      image.extract()
  return str(soup) 
