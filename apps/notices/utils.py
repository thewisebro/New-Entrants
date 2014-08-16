import re
import os
import subprocess
from BeautifulSoup import BeautifulSoup
from settings import MEDIA_ROOT, PROJECT_ROOT

PeopleProxyUrl = "http://people.iitr.ernet.in/"

def email_html_parser(html):
  soup = BeautifulSoup(html)
  links = soup('a')
  for link in links:
    if link.has_key('href'):
      link['href'] = link['href'].replace(' ','%20')
      link_href_splits = link['href'].split('/')
      if link_href_splits[0] == '':
        link['href'] = PeopleProxyUrl+'media_notices/'+'/'.join(link_href_splits[3:])
  images = soup('img')
  for image in images:
    if image.has_key('src'):
      image['src'] = image['src'].replace(' ','%20')
  first = soup.first()
  if first.name == 'p':
    first['style'] = (first['style']+';' if first.has_key('style') else '') + 'margin:0px'
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
    img['style'] = (img['style']+';' if img.has_key('style') else '') + 'max-width:670px;height:auto'
    img_src_splits = img['src'].split('/')
    if img_src_splits[0] == '':
      img['src'] = PeopleProxyUrl+'media_notices/'+'/'.join(img_src_splits[3:])
  return str(soup)

def html_parsing_while_uploading(html):
    print "Entered html_parsing_while_uploading"
    soup = convert_pdf_to_img(html)
    links = soup('a')
    for link in links:
      if link.has_key('href'):
        link['href'] = link['href'].replace(' ','%20')
    images = soup('img')
    for image in images:
      if image.has_key('src'):
        image['src'] = image['src'].replace(' ','%20')
    return str(soup)

def convert_pdf_to_img(html):
    print "Entered convert_pdf_to_img"
    match = re.compile('\.(pdf)')   #find ".pdf" in a string
    soup = BeautifulSoup(html)      # parse page content
    for link in soup.findAll('a'):      # check links
      try:
          link['href'] = link['href'].replace('%20',' ')
          href = link['href']
          print href
          # import ipdb;ipdb.set_trace()
          if re.search(match, href):
            filename = os.path.splitext(os.path.basename(href))[0]
            cmd = ['convert','-append','-density','300','-resize','1024x','-trim',PROJECT_ROOT +  href,'-quality','100','-sharpen','0x1.0','' + MEDIA_ROOT + 'notices/pdfimages/'+filename+'.png']
            subprocess.Popen(cmd)
            print "hello"
            insert_img_in_parent_html(link,filename)
      except Exception,e:
          print e
          pass
      print "hello1"
      print soup
    return soup

def insert_img_in_parent_html(element, filename):
    ix= element.parent.contents.index(element)
    showimage = element.prettify()+"<img src=\"" + "/media/notices/pdfimages/"+filename+".png\" width='900px' height='auto'>"
    element.parent.insert(ix,BeautifulSoup(showimage))
    print element.parent
    element.extract()

def remove_pdfimages(html):
    soup = BeautifulSoup(html)
    images = soup('img')
    starting = "/media/notices/pdfimages/"
    for image in images:
      if image.has_key('src') and image['src'][:len(starting)] == starting:
        image.extract()
    print soup
    return str(soup)
