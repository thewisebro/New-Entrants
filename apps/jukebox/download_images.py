"""import os
import sys
path= '/'.join(os.getcwd().split('/')[:3])
sys.path.append(path+'/channeli')
from django.core.management import setup_environ
import settings
setup_environ(settings)
"""

from BeautifulSoup import BeautifulSoup
from HTMLParser import HTMLParser

from urlparse import urlparse
import urllib2
import urllib
import re
import os
import wget
import socket
import json

from jukebox.models import *

from django.core.files import File
from django.core.files.temp import NamedTemporaryFile


def add_error(err,line):
  try:
    error = open('/home/pankaj/jukebox_scripts/new/images/images_artist_error.txt','a+')
    htm = HTMLParser()
    error.write(str(err)+'\t'+str(htm.unescape(line))+'\n')
    error.close()
  except:
    pass

def get_album_art(album):
  if(album.album_art):
    return
  url = "https://ajax.googleapis.com/ajax/services/search/images?v=1.0&q="+urllib.quote_plus(album.album)+"+album+art"
  url = urllib2.urlopen(url,timeout=5).read(10000000)
  js = json.loads(url)
  a=js['responseData']['results'][0]['url']
  img_temp = NamedTemporaryFile(delete=True)
  img_temp.write(urllib2.urlopen(a).read(600000000))
  img_temp.flush()

  name = urlparse(a).path.split('/')[-1]
  album.album_art.save(name, File(img_temp), save=True)
  print album.album, album.album_art.name

def get_artist_pic(artist):
  if(artist.cover_pic):
    return
  url = "https://ajax.googleapis.com/ajax/services/search/images?v=1.0&q="+urllib.quote_plus(artist.artist)+"+high+resolution"
  url = urllib2.urlopen(url,timeout=5).read(10000000)
  js = json.loads(url)
  minwidth = 10000
  minurl = ""
  for result in js['responseData']['results']:
    width = int(result['width'])
    if(width<minwidth and width>=1200):
      minwidth = width
      minurl = result['url']
  if(minwidth == 10000):
    minurl = js['responseData']['results'][0]['url']
  img_temp = NamedTemporaryFile(delete=True)
  img_temp.write(urllib2.urlopen(minurl).read(600000000))
  img_temp.flush()

  name = urlparse(minurl).path.split('/')[-1]
  artist.cover_pic.save(name, File(img_temp), save=True)
  print artist.artist, '      ', artist.cover_pic.name



def work_albums():
  albums = Album.objects.all()
  for album in albums:
    try:
      get_album_art(album)
    except Exception as e:
      print album.album
      print "\nErr:",e
      add_error(e,album.album)


def work_artists():
  artists = Artist.objects.all()
  for artist in artists:
    try:
      get_artist_pic(artist)
    except Exception as e:
      print artist.artist
      print "\nErr:",e
      add_error(e,artist.artist)
